"""Exceptions specific to gdaxcli."""

class Error(Exception):
  """Generic error class."""

class InvalidOrderError(Error):
  """Raised when order is invalid."""
