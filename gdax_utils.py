"""Wrapper around gdax-python.

Gdax-python is the unofficial python library for GDAX.
  https://github.com/danpaquin/gdax-python
  https://pypi.python.org/pypi/gdax
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import functools
import logging
import string

import gdax

import config

DIGITS = set(string.digits)

class Client(object):
  """Wrapper of the gdax-python library."""

  def __init__(self):
    """Initializer."""
    self._client = gdax.AuthenticatedClient(
        key=config.KEY, b64secret=config.SECRET, passphrase=config.PASSPHRASE)
    # TODO: configure sandbox keys.
    # TODO: allow public client.

  def products(self):
    """Lists products available for trading."""
    print('Product')
    for product in self._get_product_ids():
      print(product)

  def ticker(self, product_ids=None):
    # TODO: Configure default products or currencies e.g. USD only, ETH only.
    header = [
      'Product   ',
      'Price     ',
      'Size      ',
      'Bid       ',
      'Ask       ',
      'Gap       ',
      '24h Open  ',
      '24h High  ',
      '24h Low   ',
      '24h Gain (%)  ',
      '24h Volume    ',
    ]
    print(' '.join(header))
    if product_ids is None:
      product_ids = self._get_product_ids()
    for product_id in product_ids:
      tick = self._client.get_product_ticker(product_id)
      gap = float(tick['ask']) - float(tick['bid'])
      stats = self._client.get_product_24hr_stats(product_id)
      gain = float(tick['price']) - float(stats['open'])
      gain_perc = gain / float(stats['open']) * 100
      parts = [
        '%-10s' % product_id,
        '%10s' % self._truncate(tick['price'], 2),
        '%10s' % self._truncate(tick['size'], 4),
        '%10s' % self._truncate(tick['bid'], 2),
        '%10s' % self._truncate(tick['ask'], 2),
        '%10s' % self._truncate('%.6f' % gap, 2),
        '%10s' % self._truncate(stats['open'], 2),
        '%10s' % self._truncate(stats['high'], 2),
        '%10s' % self._truncate(stats['low'], 2),
        '%6s (%s)' % (self._truncate(gain, 2), self._truncate(gain_perc, 1)),
        '%14s' % self._truncate(tick['volume'], 4)]
      print(' '.join(parts))

  def balance(self):
    print('Currency  Balance')
    accounts = self._client.get_accounts()
    accounts.sort(key=lambda acc: acc['currency'])
    for account in accounts:
      avail = account['available']
      bal = account['balance']
      hold = account['hold']
      currency = account['currency']
      # TODO: allow other fiat currency. Default to usd but make it configurable.
      accuracy = 2 if currency == 'USD' else 4
      parts = [
        '%-10s' % account['currency'],
        self._truncate(avail, accuracy),
      ]
      if avail != bal:
        parts.append(' (%s - %s)' % (
            self._truncate(bal, accuracy), self._truncate(hold, accuracy)))
      print(''.join(parts))

  def history(self, accounts):
    account_ids = [(acc['id'], acc['currency'])
        for acc in self._client.get_accounts() if acc['currency'] in accounts]
    for index, data in enumerate(account_ids):
      id_, currency = data
      accuracy = 2 if currency == 'USD' else 4
      if index != 0:
        print()
      print('Account: %s' % currency)
      print(' '.join([
        'Type                ',
        'Amount    ',
        'Balance   ',
        'Product   ',
        'Date      ',
      ]))
      for page in self._client.get_account_history(id_):
        for item in page:
          type_ = item['type']
          product = ''
          if type_ == 'transfer':
            transfer_type = item['details']['transfer_type']
            type_ = 'transfer (%s)' % transfer_type
          elif type_ == 'match':
            product = item['details']['product_id']
          print(' '.join([
            '%-20s' % type_,
            '%10s' % self._truncate(item['amount'], accuracy),
            '%10s' % self._truncate(item['balance'], accuracy),
            '%10s' % product,
            # TODO: convert date to local date.
            '%-20s' % item['created_at'],
          ]))

  def orders(self):
    pages = self._client.get_orders()
    print(' '.join([
      'Side      ',
      'Size      ',
      'Size (USD)',
      'Filled    ',
      'Price     ',
      'Fees      ',
      'Status    ',
      'Date placed'
    ]))
    for page in pages:
      for order in page:
        size_usd = float(order['size']) * float(order['price'])
        fees = self._truncate(order['fill_fees'], 2)
        print(' '.join([
          '%-10s' % order['side'],
          '%10s' % self._truncate(order['size'], 4),
          '%10s' % self._truncate(str(size_usd), 2),
          '%10s' % self._truncate(order['filled_size'], 4),
          '%10s' % self._truncate(order['price'], 2),
          '%10s' % fees,
          '%10s' % order['status'],
          '%20s' % order['created_at'],
        ]))
        # TODO: local date.

  def order(self, order_type, side, product, size, price):
    """Place an order.

    Args:
      order_type: One of limit, market or stop.
      side: One of buy or sell.
      product: The product to be exchanged. Can be uppercased or lowercased.
          For example: eth-usd, BTC-GBP, ...
      size: The amount to buy or sell. Can be coin or fiat.
      price: Price to place limit/stop order. Ignored if order type is market.
          Price can be relative to the current ticker price by prepending
          the difference amount with + or - . Order is checked to make sure
          you're not buying higher or selling lower than current price.
    """
    product = product.upper()
    self._check_valid_order(
        order_type, side, product, size, price)

    # TODO: make this configurable
    self_trade_prevention = True
    func = self._client.buy if side == 'buy' else self._client.sell
    func = functools.partial(func, product_id=product, type=order_type, side=side,
                             size=size, stp=self_trade_prevention)

    current_price = float(self._client.get_product_ticker(product)['price'])

    if order_type == 'market':
      logging.info('Placing market order: %s %s @ %.2f',
                   side, size, current_price)
      func()

    elif order_type == 'limit':
      abs_price, amount = self._parse_price(price, current_price)
      if side == 'buy' and amount >= 0:
        raise ValueError(
            'Buying higher than or equal to current price: %s >= %.2f' % (
            abs_price, current_price))
      elif side == 'sell' and amount <= 0:
        raise ValueError(
            'Selling lower than or equal to current price: %s <= %.2f' % (
            abs_price, current_price))
      logging.info('Placing limit order: %s %s @ %s (%.2f)',
                   side, size, abs_price, float(abs_price) - current_price)
      # TODO: make time_in_force, post_only configurable.
      func(price=abs_price)

    elif order_type == 'stop':
      # TODO
      raise NotImplementedError('This functionality is not yet implemented.')

  def _parse_price(self, price, current_price):
    # TODO: make default diff amount configurable.

    if price[0] in DIGITS:
      # Absolute price.
      return (self._truncate(price, 2), float(price) - current_price)

    # Relative price.
    amount = float(price[1:])
    if price.startswith('-'):
      amount = -amount
    abs_price = current_price + amount
    # If we simply call str, it may return a scientific notation e.g. 5e-5.
    return (self._truncate('%.6f' % abs_price, 2), amount)

  def _check_valid_order(
      self, order_type, side, product, size, price):
    product = product.upper()
    product_ids = self._get_product_ids()
    # TODO: throw more meaningful error messages.
    assert order_type in {'market', 'limit', 'stop'}
    assert side in {'buy', 'sell'}
    assert product in product_ids
    float(size)
    if order_type != 'market':
      assert price[0] in (DIGITS | {'-', '+'})

  def _get_product_ids(self):
    """Gets sorted list of products."""
    products = self._client.get_products()
    product_ids = [p['id'] for p in products]
    product_ids.sort()
    return product_ids

  def _truncate(self, s, digits):
    """Truncate the value to the number of digits after the dot specified.

    We don't round up because rounding up can cause issues. For example you have
    0.1111115 BTC, but rounding up could show 0.111112, which exceeds the actual
    amount when you try to sell all of it.
    """
    if not isinstance(s, str):
      s = str(s)
    for index, char in enumerate(s):
      if char == '.':
        dot_index = index
        end = dot_index + digits + 1
        break
    else:
      end = len(s)
    return s[:end]
