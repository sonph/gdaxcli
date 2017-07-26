"""Wrapper around gdax-python.

Gdax-python is the unofficial python library for GDAX.
  https://github.com/danpaquin/gdax-python
  https://pypi.python.org/pypi/gdax
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# OrderedDict retains its key order, so we get consistent column ordering.
from collections import OrderedDict
import functools
import logging
import string
import sys
import traceback

# https://pypi.python.org/pypi/colorama
import colorama
colorama.init()

# https://pypi.python.org/pypi/tabulate
from tabulate import tabulate

try:
  import gdax
  # TODO: include other non-standard libraries in this as well.
except ImportError:
  traceback.print_exc()
  print('Unable to import gdax. Make sure you follow the installation'
        ' instructions at https://github.com/sonph/gdaxcli')
  sys.exit(1)

try:
  import config
except ImportError:
  traceback.print_exc()
  print('Unable to import configurations. Make sure you follow the instructions'
        ' for configuring API keys at https://github.com/sonph/gdaxcli')
  sys.exit(1)

DIGITS = set(string.digits)

# TODO: make this configurable.
DEFAULT_ACCURACY = 4

tabulate = functools.partial(tabulate,
    tablefmt='plain', headers='keys', floatfmt='.%df' % DEFAULT_ACCURACY)

negative = lambda x: float(x) < 0
nonnegative = lambda x: float(x) >= 0
positive = lambda x: float(x) > 0
nonpositive = lambda x: float(x) <= 0

def format_float(value, accuracy=DEFAULT_ACCURACY):
  """Formatting the value as a float with set number of digits after the dot.

  This is only needed if we want to colorize it or use a different number of
  digits other than the default, before adding it into the table. Otherwise,
  tabulate automatically formats the value for us.
  """
  placeholder = '%.' + str(accuracy) + 'f'
  return placeholder % float(value)

def colorize(value, condition, accuracy=None):
  """Return green string if condition is true; red otherwise.

  Args:
    value: Value to return as string. If it's a float, it will be formatted.
    condition: Either a bool or a lambda.
  """
  if isinstance(value, float):
    if accuracy is None:
      value = format_float(value)
    else:
      value = format_float(value, accuracy)

  if not isinstance(condition, bool):
    condition = condition(value)

  color = colorama.Fore.GREEN if condition else colorama.Fore.RED
  return color + value + colorama.Style.RESET_ALL

green = lambda value: colorize(value, True)
red = lambda value: colorize(value, False)

def is_str_zero(s):
  """Returns True is string s is strictly zero.

  Converting the value to float and comparing with 0 within a set threshold is
  another approach, but since gdax returns a string, why not just check it?
  """
  for char in s:
    if char in DIGITS:
      if char != '0':
        return False
  return True


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
    rows = []
    for product in self._client.get_products():
      rows.append(OrderedDict([
        ('id', product['id']),
        ('base_currency', product['base_currency']),
        ('quote_currency', product['quote_currency']),
        ('base_min_size', product['base_min_size']),
        ('base_max_size', product['base_max_size']),
        ('quote_increment', product['quote_increment']),
    ]))
    print(tabulate(rows))

  def ticker(self, product_ids=None):
    # TODO: Configure default products or currencies e.g. USD only, ETH only.
    rows = []
    if product_ids is None:
      product_ids = self._get_product_ids()
    for product_id in product_ids:
      tick = self._client.get_product_ticker(product_id)
      gap = float(tick['ask']) - float(tick['bid'])
      stats = self._client.get_product_24hr_stats(product_id)
      gain = float(tick['price']) - float(stats['open'])
      gain_perc = gain / float(stats['open']) * 100
      rows.append(OrderedDict([
        ('product_id', product_id),
        ('price', tick['price']),
        ('size', tick['size']),
        ('bid', tick['bid']),
        ('ask', tick['ask']),
        ('gap' , gap),
        ('24h_volume', tick['volume']),
        ('24h_open', stats['open']),
        ('24h_high', stats['high']),
        ('24h_low', stats['low']),
        ('24h_gain', colorize(gain, nonnegative)),
        ('perc', colorize(format_float(gain_perc, 2),
                                   nonnegative(gain_perc)))
      ]))
    print(tabulate(rows))

  def balance(self):
    rows = []
    accounts = self._client.get_accounts()
    accounts.sort(key=lambda acc: acc['currency'])
    for acc in accounts:
      hodl = acc['hold']
      rows.append(OrderedDict([
        ('currency', acc['currency']),
        ('balance', acc['balance']),
        ('available', acc['available']),
        ('hold', red(hodl) if not is_str_zero(hodl) else hodl),
      ]))
    print(tabulate(rows))

  def history(self, accounts):
    """Get trade history for specified accounts: USD, BTC, ETH, LTC, etc."""
    # TODO: allow user to specify what currency to use
    acc_ids = []

    for acc in self._client.get_accounts():
      currency = acc['currency']
      if currency in accounts:
        acc_ids.append((acc['id'], currency))

    for index, value in enumerate(acc_ids):
      acc_id, currency = value
      rows = []
      if index != 0:
        print()
      print('Account: %s' % currency)

      for page in self._client.get_account_history(acc_id):
        for item in page:
          is_green = True
          product, type_, amount = '', item['type'], float(item['amount'])
          if type_ == 'transfer':
            transfer_type = item['details']['transfer_type']
            is_green = (transfer_type == 'deposit')
            type_ = 'transfer (%s)' % transfer_type
          elif type_ == 'match':
            product = item['details']['product_id']
            is_green = nonnegative(amount)
          elif type_ == 'fee':
            is_green = False
          rows.append(OrderedDict([
            ('type', colorize(type_, is_green)),
            # TODO: fix the amount column not aligned as numbers. This is
            # probably due to the color.
            ('amount', colorize(amount, is_green)),
            ('balance', format_float(item['balance'])),
            ('product_id', product),
            ('created_at', item['created_at']),
          ]))
      print(tabulate(rows, numalign="decimal"))

  def orders(self):
    rows = []
    pages = self._client.get_orders()
    for page in pages:
      for order in page:
        size, price = float(order['size']), float(order['price'])
        size_usd = size * price
        fill_fees = order['fill_fees']
        rows.append(OrderedDict([
          ('id', order['id'][6]),
          ('product_id', order['product_id']),
          ('side', colorize(order['side'], lambda x: x == 'buy')),
          ('type', order['type']),
          ('price', price),
          ('size', size),
          ('size_usd', size_usd),
          ('filled_size', order['filled_size']),
          ('fill_fees', red(format_float(fill_fees)) if not is_str_zero(fill_fees) else float(fill_fees)),
          ('status', colorize(order['status'], lambda x: x == 'open')),
          ('time_in_force', order['time_in_force']),
          ('settled', 'yes' if order['settled'] else red('no')),
          ('stp', order['stp']),
          ('created_at', order['created_at']),
          # TODO: local date.
        ]))

    if rows:
      print(tabulate(rows))
    else:
      print('No pending orders')

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
    # TODO: read the self trade prevention option from config
    func = functools.partial(func, product_id=product, type=order_type, side=side,
                             size=size)

    current_price = float(self._client.get_product_ticker(product)['price'])

    if order_type == 'market':
      logging.info('Placing market order: %s %s @ %.2f',
                   side, size, current_price)
      print(func())

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
      print(func(price=abs_price))

    elif order_type == 'stop':
      # TODO
      raise NotImplementedError('This functionality is not yet implemented.')

  def fills(self, product=None):
    rows = []
    pages = self._client.get_fills(product_id=product)
    for page in pages:
      for fill in page:
        size, price = float(fill['size']), float(fill['price'])
        size_usd = size * price
        fee = fill['fee']
        rows.append(OrderedDict([
          ('product_id', fill['product_id']),
          ('side', colorize(fill['side'], lambda side: side == 'buy')),
          ('price', price),
          ('size', size),
          ('size_usd', size_usd),
          ('fee', red(fee) if not is_str_zero(fee) else fee),
          ('settled', 'yes' if fill['settled'] else red('no')),
          ('created_at', fill['created_at']),
        ]))
    if rows:
      print(tabulate(rows))
    else:
      print('No fills')

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
    assert order_type in set(['market', 'limit', 'stop'])
    assert side in set(['buy', 'sell'])
    assert product in product_ids
    float(size)
    if order_type != 'market':
      assert price[0] in (DIGITS | set(['-', '+']))

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

