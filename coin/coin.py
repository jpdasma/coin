# -*- coding: utf-8 -*-
# Copyright (C) 2018 Julian Paul Dasmariñas
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
import requests
import os
import logging
import json
import random
import hmac
import hashlib

from coin.exceptions import FilePermissionError

class Coin(object):
    """
    TODO: Docstring
    """
    AUTH_URL = 'https://coins.ph/user/api/authorize'
    SELLORDER_API_URL = 'https://coins.ph/api/v2/sellorder'
    MARKET_RATE_URL = 'https://quote.coins.ph/v1/markets/BTC-PHP'

    def __init__(self, *args, **kwargs):
        self.config_file_location = os.environ['HOME'] + '/.coin'
        self.config_file = self.config_file_location + '/config'
        self.logger = logging.getLogger('coin')
        self.args = args
        self.kwargs = kwargs

    def _read_config(self):
        file_mode = os.stat(self.config_file)[0]

        if file_mode != 33152:
            raise FilePermissionError("Config file must be mode 600 to ensure that only the user could read it")

        with open(self.config_file, "rb") as file_handler:
            config = map(lambda x: x.rstrip(), file_handler.readlines())
        config = dict(map(lambda x: tuple(x.split(b':')), config))
        return config

    def _generate_nonce(self, length=16):
        return ''.join([str(random.randint(0, 9)) for i in range(length)])

    def _generate_headers(self, body, url):
        config = self._read_config()
        nonce = self._generate_nonce()
        if body:
            body = json.dumps(body, separators=(',', ':'))
            message = nonce + url + body
        else:
            message = nonce + url

        signature = hmac.new(config[b'secret'], message.encode('utf-8'), hashlib.sha256).hexdigest()

        headers = {
            'ACCESS_SIGNATURE': str(signature),
            'ACCESS_KEY': config[b'api'].decode('utf-8'),
            'ACCESS_NONCE': nonce,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        return headers

    def _php_to_btc(self, php=1):
        value = json.loads(requests.get(self.MARKET_RATE_URL).text)
        btc = int(value['market']['bid'])
        return format(php * (1 / btc), '.7f')

    def config(self):
        """
        TODO: Docstring
        """
        api_key = input("API Key: ")
        secret = input("Secret: ")

        try:
            os.mkdir(self.config_file_location, mode=0o700)
        except FileExistsError:
            os.chmod(self.config_file_location, 0o700)
            self.logger.info('Directory {} already exists'.format(self.config_file_location))

        config = 'api:{}\nsecret:{}\n'.format(api_key, secret)

        with open(self.config_file, "w") as file_handler:
            file_handler.write(config)

        os.chmod(self.config_file, 0o600)
 
    def buy_load(self, phone_number, amount, network):
        """
        TODO: Docstring
        """
        body = {
            "payment_outlet": "load-" + network,
            "btc_amount": float(self._php_to_btc(amount)),
            "currency": "PHP",
            "currency_amount_locked": amount,
            "pay_with_wallet": "BTC",
            "phone_number_load": phone_number
        }
        headers = self._generate_headers(body, self.SELLORDER_API_URL)
        requests.post(self.SELLORDER_API_URL, headers=headers, data=body)
