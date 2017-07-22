import logging
import sys

import gdax_utils
import utils

COMMANDS = {'products'}

def usage():
  """Usage: gdaxcli <command> [arguments]
      products                      Lists products available for trading.
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

  if cmd == 'products':
    client.get_products()

if __name__ == '__main__':
  utils.configure_logging(to_file=False)
  main()
