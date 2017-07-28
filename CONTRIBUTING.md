# Contributing

Contributions are welcome. For large changes, please open issues to discuss before you send in PRs
to avoid wasting efforts.

## Development environment

You can either use [`pipenv`][1] just `pip` to setup dependencies:

```
pip install pipenv
pip install --dev
```

If you use `pip`, make sure you also install `mock` for unittests:

```
pip install mock
```

## Sandbox

You can use the gdax sandbox for testing orders. The API responses aren't exactly like the
production API, so it's too much of a pain to make the tool work with all the quirks of the sandbox.
This remains a **TODO**.

For now you can test read-only commands like `balance, orders, fills, products, etc.` with the prod
API.

The `--sandbox` flag is not added yet, but in the mean time:

1. Put your sandbox keys in `~/.gdaxconfig_cli.sandbox`
2. Update the `gdax_utils.Client.__init__` method to
  - `config = utils.read_config('~/.gdaxcli_config.sandbox')`
  - `gdax.AuthenticatedClient(..., api_url="https://api-public.sandbox.gdax.com")`

## References

  - [Google python style guide][2]: not strictly enforced, but good to follow.
  - [GDAX API docs][3]
  - [`gdax-python` library][4]
  - [`python-tabulate` library][5] or [github mirror][6]
  - [`colorama` library][7]

[1]: https://github.com/kennethreitz/pipenv
[2]: https://google.github.io/styleguide/pyguide.html
[3]: https://docs.gdax.com/
[4]: https://github.com/danpaquin/gdax-python
[5]: https://bitbucket.org/astanin/python-tabulate
[6]: https://github.com/sonph-forks/python-tabulate
[7]: https://github.com/tartley/colorama
