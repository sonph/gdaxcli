# GdaxCli

[![travis-build-badge][7]][8]

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
```

## Configuring

To obtain an API key for your account to be used with this tool:

  1. Login to your GDAX account
  2. Go to **Settings** > **API** or [https://www.gdax.com/settings/api][4]
  3. Select the **trade** permission and generate an API key
  4. Run `bash make.sh configure` and copy paste the passphrase, key and secret accordingly

See [gdax docs][5] for more information on the API key.

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
[7]: https://travis-ci.org/sonph/gdaxcli.svg?branch=master
[8]: https://travis-ci.org/sonph/gdaxcli
