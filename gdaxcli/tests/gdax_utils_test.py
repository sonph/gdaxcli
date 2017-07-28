"""Unit tests."""

import unittest

import mock

from .. import gdax_utils
from .. import utils

utils.configure_logging(to_stderr=True, to_file=False)

class TestInit(unittest.TestCase):
  def setUp(self):
    self.patcher = mock.patch('gdax.AuthenticatedClient', autospec=True)
    self.mock_gdax_client_class = self.patcher.start()
    self.mock_client = mock.Mock(spec=self.mock_gdax_client_class)
    self.mock_gdax_client_class.return_value = self.mock_client

    self.mock_client.get_products.return_value = [
      {'id': 'ETH-USD'},
      {'id': 'BTC-GBP'},
    ]

    self.mock_client.get_product_ticker.return_value = {'price': '123.45'}

    self.c = gdax_utils.Client()

  def tearDown(self):
    self.patcher.stop()

  def testGetProductIds(self):
    self.assertListEqual(self.c._get_product_ids(), ['BTC-GBP', 'ETH-USD'])

  def testCheckValidOrder(self):
    # order_type, side, product, size, price, product_ids
    self.c._check_valid_order('limit', 'buy', 'ETH-USD', '23.4', '140.11')
    self.c._check_valid_order('market', 'sell', 'btc-gbp', '948.2', '1239123')
    self.c._check_valid_order('market', 'sell', 'btc-gbp', '5', '-2')
    # TODO: test stop orders.
    with self.assertRaises(AssertionError):
      self.c._check_valid_order('something', 'buy', 'ETH-USD', '23.4', '140.11')
    with self.assertRaises(AssertionError):
      self.c._check_valid_order('something', 'buysell', 'ETH-USD', '23.4', '140.11')
    with self.assertRaises(AssertionError):
      self.c._check_valid_order('something', 'buysell', 'usd-gbp', '23.4', '140.11')
    with self.assertRaises(AssertionError):
      self.c._check_valid_order('limit', 'buysell', 'usd-gbp', '23.4', '')

  def testParsePrice(self):
    test_values = [
      ('-1', ('122.45', -1)),
      ('-1.00', ('122.45', -1)),
      ('+.5', ('123.95', 0.5)),
      ('+5', ('128.45', 5.0)),
      ('+99.11', ('222.56', 99.11)),
      # Maybe flaky here if we use assertEqual
      ('180', ('180', 180 - 123.45)),
      ('50', ('50', 50 - 123.45)),
      ('45.87', ('45.87', 45.87 - 123.45)),
    ]
    for price, abs_price in test_values:
      self.assertEqual(self.c._parse_price(price, 123.45), abs_price)

  def testTruncate(self):
    test_values = [
      (('123.45', 1), '123.4'),
      (('1234.5678', 2), '1234.56'),
      (('1234.5678', 3), '1234.567'),
      (('1234.5678', 4), '1234.5678'),
    ]
    for args, expected in test_values:
      self.assertEqual(self.c._truncate(*args), expected)

  def testOrder(self):
    # order_type, side, product, size, price
    self.c.order('market', 'buy', 'eth-usd', '0.1', '', skip_confirmation=True)
    self.c.order('limit', 'buy', 'ETH-USD', '.25', '-1', skip_confirmation=True)
    with self.assertRaises(ValueError):
      self.c.order('limit', 'buy', 'ETH-USD', '9.3', '125',
                   skip_confirmation=True)
    with self.assertRaises(ValueError):
      self.c.order(
          'limit', 'buy', 'ETH-USD', '9.3', '+1', skip_confirmation=True)

    kwargs = {
        'side': 'buy',
        'product_id': 'ETH-USD',
    }
    self.mock_client.buy.assert_has_calls([
      mock.call(type='market', size='0.1', **kwargs),
      mock.call(type='limit', size='.25', price='122.45', **kwargs),
    ])

    self.c.order(
        'market', 'sell', 'ETH-USD', '.2345', None, skip_confirmation=True)
    self.c.order(
        'limit', 'sell', 'ETH-USD', '0.1', '180', skip_confirmation=True)
    with self.assertRaises(ValueError):
      self.c.order(
          'limit', 'sell', 'ETH-USD', '0.1', '120', skip_confirmation=True)
    with self.assertRaises(ValueError):
      self.c.order(
          'limit', 'sell', 'ETH-USD', '0.1', '123.43', skip_confirmation=True)
    with self.assertRaises(ValueError):
      self.c.order(
          'limit', 'sell', 'ETH-USD', '0.1', '-.5', skip_confirmation=True)

    kwargs['side'] = 'sell'
    self.mock_client.sell.assert_has_calls([
      mock.call(type='market', size='.2345', **kwargs),
      mock.call(type='limit', size='0.1', price='180', **kwargs),
    ])

if __name__ == '__main__':
  unittest.main()
