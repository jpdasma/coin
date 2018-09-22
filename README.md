# coin

coins.ph command line tool.

You would need to get a developers api since this is currently using HMAC for authentication.

## Usage

```
[local@localhost]$ coin-cmd --help
Usage: coin-cmd [OPTIONS] COMMAND [ARGS]...

  coins.ph command line tool

Options:
  --help  Show this message and exit.

Commands:
  buy_load  Buy a load using your coins.ph account.
  config    Setup the API and Secret key in a config...
```

Initialize config file:

```
coin-cmd config
```

Buy load:

```
coin-cmd buy_load [OPTIONS] PHONE_NUMBER AMOUNT NETWORK

[local@localhost]$ coin-cmd buy_load +639151111111 100 globe
```

## To Do

1. Add other features from coins.ph (Transfer money, convert money)
2. Automatically detect the network based on the phone number
3. Use OAUTH instead of HMAC
