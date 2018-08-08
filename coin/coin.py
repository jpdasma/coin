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

from coin.exceptions import FilePermissionError

class Coin(object):
    """
    TODO: Docstring
    """
    SELLORDER_API_URL = 'https://coins.ph/api/v2/sellorder'

    def __init__(self, *args, **kwargs):
        self.config_file_location = os.environ['HOME'] + '/.coin'
        self.config_file = self.config_file_location + '/config'
        self.logger = logging.getLogger('coin')
        self.args = args
        self.kwargs = kwargs

    def _read_config(self):
        file_mode = os.stat(self.config_file)[0]

        if file_mode != 33152:
            raise FilePermissionError("Config file must be mode 700 to ensure that only the user could read it")

        with open(self.config_file, "r") as file_handler:
            config = map(lambda x: x.rstrip(), file_handler.readlines())
        config = dict(map(lambda x: tuple(x.split(':')), config))
        return config

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

    def buy_load(self, phone_number):
        """
        TODO: Docstring
        """
        pass
