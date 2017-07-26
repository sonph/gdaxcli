import logging
import sys

import gdax_utils
import utils

def usage():
  # TODO: Maybe add short commands e.g. t, h, o, ...
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
      fills [product]               Get recent fills.
  """

def main():
  try:
    cmd = sys.argv[1]
  except IndexError:
    print(usage.__doc__)
    sys.exit()

  client = gdax_utils.Client()

  try:
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
      # TODO: add confirmation and option to skip -y/--yes
      try:
        order_type = sys.argv[2]
        side = sys.argv[3]
        product = sys.argv[4]
        size = sys.argv[5]
        price = sys.argv[6] if len(sys.argv) == 7 else None
      except IndexError:
        raise ValueError('Missing a required value')
      client.order(order_type, side, product, size, price)
    elif cmd == 'fills':
      client.fills()
    else:
      logging.error('Invalid command: %s', cmd)
      sys.exit(1)
  except Exception as e:
    import traceback
    traceback.print_exc()
    print('GETTING AN ERROR? File it at https://github.com/sonph/gdaxcli/issues')

if __name__ == '__main__':
  utils.configure_logging(to_file=False)
  main()
