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
import unittest
import os
import shutil
import tempfile
import random
import hmac
import requests

from unittest.mock import MagicMock, patch
from coin.coin import Coin
from coin.exceptions import FilePermissionError

def mocked_requests_get(*args, **kwargs):
    class MockResponse(object):
        def __init__(self, text, status_code):
            self.text = text
            self.status_code = status_code
        def text(self):
            return self.text
    return MockResponse('{"market": { "ask": "359173", "bid": "345087", "currency": "PHP", "expires_in_seconds": 20, "product": "BTC", "symbol": "BTC-PHP" }}', 200)


class TestCoin(unittest.TestCase):

    def setUp(self):
        self.coin = Coin()

    @patch('builtins.input')
    def test__config(self, mock_input):
        mock_input.side_effect = [ 'apikey111', 'secretkey222' ]
        self.coin.config()
        dir_mod = os.stat(os.environ['HOME'] + '/.coin')[0]
        file_mod = os.stat(os.environ['HOME'] + '/.coin/config')[0]
        self.assertEquals(16832, dir_mod)
        self.assertEquals(33152, file_mod)
        with open(os.environ['HOME'] + '/.coin/config', 'r') as file_handler:
            config = file_handler.read()
        self.assertEquals('api:apikey111\nsecret:secretkey222\n', config)

    @patch('builtins.input')
    def test___read_config(self, mock_input):
        mock_input.side_effect = [ 'apikey111', 'secretkey222' ]
        self.coin.config()
        self.assertEquals({b'api':b'apikey111', b'secret':b'secretkey222'}, self.coin._read_config())

    @patch('builtins.input')
    def test___read_config_filepermissionerror(self, mock_input):
        mock_input.side_effect = [ 'apikey111', 'secretkey222' ]
        self.coin.config()
        os.chmod(os.environ['HOME'] + '/.coin/config', 0o777)
        self.assertRaises(FilePermissionError, self.coin._read_config)

    @patch('random.randint')
    def test___generate_nonce(self, mock_randint):
        mock_randint.side_effect = [ 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6 ]
        nonce = self.coin._generate_nonce()
        self.assertEquals('1234567890123456', nonce)

    @patch('builtins.input')
    @patch('hmac.HMAC.hexdigest')
    @patch('random.randint')
    def test___generate_headers(self, mock_randint, mock_hexdigest,  mock_input):
        mock_input.side_effect = [ 'apikey111', 'secretkey222' ]
        mock_hexdigest.return_value = 'test'
        mock_randint.side_effect = [ 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6 ]
        self.coin.config()
        body = ""
        url = "http://test.com/api/v1/"
        header = self.coin._generate_headers(body, url)
        self.assertEquals({ 'ACCESS_SIGNATURE': 'test', 'ACCESS_KEY': 'apikey111', 'ACCESS_NONCE': '1234567890123456', 'Content-Type': 'application/json', 'Accept': 'application/json'}, header)

    @patch('requests.get', side_effect=mocked_requests_get)
    def test___php_to_btc(self, mock_get):
        value = self.coin._php_to_btc(25)
        self.assertEquals('0.0000724', value)

    @patch('builtins.input')
    @patch('hmac.HMAC.hexdigest')
    @patch('random.randint')
    @patch('requests.get', side_effect=mocked_requests_get)
    @patch('requests.post')
    def test__buy_load(self, mock_post, mock_get, mock_randint, mock_hexdigest,  mock_input):
        mock_input.side_effect = [ 'apikey111', 'secretkey222' ]
        mock_hexdigest.return_value = 'test'
        mock_randint.side_effect = [ 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6 ]
        self.coin.config()
        self.coin.buy_load('111', 25, "globe")
        mock_post.assert_called_with('https://coins.ph/api/v2/sellorder', data={'payment_outlet': 'load-globe', 'btc_amount': 7.24e-05, 'currency': 'PHP', 'currency_amount_locked': 25, 'pay_with_wallet': 'BTC', 'phone_number_load': '111'}, headers={'ACCESS_SIGNATURE': 'test', 'ACCESS_KEY': 'apikey111', 'ACCESS_NONCE': '1234567890123456', 'Content-Type': 'application/json', 'Accept': 'application/json'})


if __name__ == '__main__':
    unittest.main()
