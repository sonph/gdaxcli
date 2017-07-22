"""Utilities."""

import logging

def configure_logging(to_stderr=True, to_file=True, file_name='main.log'):
  """Configure logging destinations."""
  root_logger = logging.getLogger()
  root_logger.setLevel(logging.INFO)

  format_str = '%(asctime)s - %(levelname)s - %(message)s'
  formatter = logging.Formatter(format_str)

  if to_stderr:
    stderr_handler = logging.StreamHandler()
    stderr_handler.setFormatter(formatter)
    root_logger.addHandler(stderr_handler)

  if to_file:
    file_handler = logging.FileHandler(file_name)
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)
