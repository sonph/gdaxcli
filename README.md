# GdaxCli

A commandline client for cryptocurrency trading on [GDAX][1] (Global Digital Assets Exchange).

Work in progress.

## Usage

```
Usage: gdaxcli <command> [arguments]
    products                      Lists products available for trading.
    ticker [product1 product2..]  Get current market ticker.
    balance                       Get account balance.
    history [account1 account2..] Get account history (transfer, match, fee, rebate).
                                  Default USD.
```

## Configuring

To obtain an API key for your account to be used with this tool:

  1. Login to your GDAX account
  2. Go to **Settings** > **API** or [https://www.gdax.com/settings/api][4]
  3. Generate an API key with **trade** permission
  4. Copy `[config.example.py](config.example.py)` to `config.py` and copy these three things from
  the website into the file:
    - the key
    - the secret
    - the passphrase

so it looks like this:

(file `config.py`)
```
PASSPHRASE = 'ts2an3wj1'
KEY = 'tyeg0pwwv60x2oipzl2r5osfzidtppd'
SECRET = 'bGFza2pkZjtoZWkyODM5NHkybGtmbHN5ZGY4MjNomxrZHNmYWFhZGZ3MTIzMTJhZA=='
```

Remember, it's a secret, so don't let anyone else know. See [gdax docs][5] for more information on
API key.

**TODO**: mention the sandbox

## Contributing

See [CONTRIBUTING][3].

## License

DISCLAIMER: No warranty is provided for this software. Use it at your own risk.

Code is released under [the MIT License][2].

Remember:

> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
> IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
> FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
> AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
> LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
> OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
> SOFTWARE.

[1]: https://www.gdax.com/
[2]: https://choosealicense.com/licenses/mit/
[3]: CONTRIBUTING.md
[4]: https://www.gdax.com/settings/api
[5]: https://docs.gdax.com/#generating-an-api-key
[6]: https://public.sandbox.gdax.com
