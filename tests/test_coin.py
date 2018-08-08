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

from unittest.mock import MagicMock, patch
from coin.coin import Coin
from coin.exceptions import FilePermissionError

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
        self.assertEquals({'api':'apikey111', 'secret':'secretkey222'}, self.coin._read_config())

    @patch('builtins.input')
    def test___read_config_filepermissionerror(self, mock_input):
        mock_input.side_effect = [ 'apikey111', 'secretkey222' ]
        self.coin.config()
        os.chmod(os.environ['HOME'] + '/.coin/config', 0o777)
        self.assertRaises(FilePermissionError, self.coin._read_config)


if __name__ == '__main__':
    unittest.main()
