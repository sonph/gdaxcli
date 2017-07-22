import logging
import sys

import gdax_utils
import utils

# TODO: Maybe use short commands e.g. t, h, o, ...
COMMANDS = {'products', 'ticker', 'help'}

def usage():
  """Usage: gdaxcli <command> [arguments]
      products                      Lists products available for trading.
      ticker [product1 product2..]  Get current market ticker.
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
  if cmd == 'products':
    client.products()
  if cmd == 'ticker':
    products = sys.argv[2:] if len(sys.argv) > 2 else None
    client.ticker(products)

if __name__ == '__main__':
  utils.configure_logging(to_file=False)
  main()
