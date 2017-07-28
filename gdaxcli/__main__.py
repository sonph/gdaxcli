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

      fills [product]               Get recent fills.

      order list                    List open orders
      orders

      orders cancel <product>       Cancel all orders.
      order cancel all <product>

      order cancel <id>             Cancel order. Id can be a short prefix.

      order <limit/market/stop> <buy/sell> <product> <size> [price]
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
      if len(sys.argv) > 2 and sys.argv[2] == 'cancel':
        product = sys.argv[3]
        client.cancel_all(product)
      else:
        client.orders()
    elif cmd == 'order':
      # TODO: add confirmation and option to skip -y/--yes
      try:
        order_type = sys.argv[2]
        if order_type == 'cancel':
          order_id = sys.argv[3]
          if order_id == 'all':
            product = sys.argv[4]
            client.cancel_all(product)
          else:
            client.order_cancel(order_id)
        elif order_type == 'list':
          client.orders()
        else:
          side = sys.argv[3]
          product = sys.argv[4]
          size = sys.argv[5]
          price = sys.argv[6] if len(sys.argv) == 7 else None
          client.order(order_type, side, product, size, price)
      except IndexError:
        logging.error('Missing required value.')
        print(usage.__doc__)
        sys.exit()
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
