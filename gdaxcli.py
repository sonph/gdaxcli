import logging
import sys

import gdax_utils
import utils

# TODO: Maybe use short commands e.g. t, h, o, ...
COMMANDS = {'balance', 'products', 'ticker', 'balance', 'history', 'orders'}

def usage():
  """Usage: gdaxcli <command> [arguments]
      products                      Lists products available for trading.
      ticker [product1 product2..]  Get current market ticker.
      balance                       Get account balance.
      history [account1 account2..] Get account history (transfer, match, fee, rebate).
                                    Default USD.
      orders                        List open orders.
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

if __name__ == '__main__':
  utils.configure_logging(to_file=False)
  main()
