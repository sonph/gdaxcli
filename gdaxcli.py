import logging
import sys

import gdax_utils
import utils

# TODO: Maybe use short commands e.g. t, h, o, ...
COMMANDS = {
    'balance', 'products', 'ticker', 'balance', 'history', 'orders', 'order'}

def usage():
  """Usage: gdaxcli <command> [arguments]
      products                      Lists products available for trading.
      ticker [product1 product2..]  Get current market ticker.

      balance                       Get account balance.
      history [account1 account2..] Get account history (transfer, match, fee, rebate).
                                        Default USD.

      orders                        List open orders.
      order limit/market/stop buy/sell product size [price]
                                    Place an order. Limit price can be absolute or
                                        relative such as 180, 180.23, -1, +.5
                                        Product can be uppercased or lowercased.
                                        For example: eth-usd, BTC-GBP, ..
  """

def main():
  try:
    cmd = sys.argv[1]
  except IndexError:
    print(usage.__doc__)
    sys.exit()

  if cmd not in COMMANDS:
    logging.error('Invalid command: %s', cmd)
    sys.exit(1)

  client = gdax_utils.Client()

  if cmd == 'help':
    print(usage.__doc__)
  elif cmd == 'products':
    client.products()
  elif cmd == 'ticker':
    products = sys.argv[2:] if len(sys.argv) > 2 else None
    client.ticker(products)
  elif cmd == 'balance':
    client.balance()
  elif cmd == 'history':
    accounts = sys.argv[2:] if len(sys.argv) > 2 else ['USD']
    client.history(accounts)
  elif cmd == 'orders':
    client.orders()
  elif cmd == 'order':
    try:
      order_type = sys.argv[2]
      side = sys.argv[3]
      product = sys.argv[4]
      size = sys.argv[5]
      price = sys.argv[6] if len(sys.argv) == 7 else None
    except IndexError:
      raise ValueError('Missing a required value')
    client.order(order_type, side, product, size, price)

if __name__ == '__main__':
  utils.configure_logging(to_file=False)
  main()
