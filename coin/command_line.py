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
import click
from .coin import Coin


@click.group()
def main():
    """coins.ph command line tool
    """
    pass

@click.command()
def config():
    """Setup the API and Secret key in a config file.
    """
    coin = Coin()
    coin.config()

@click.command()
@click.argument('phone_number')
@click.argument('amount')
@click.argument('network')
def buy_load(phone_number, amount, network):
    """Buy a load using your coins.ph account.
    """
    coin = Coin()
    coin.buy_load(phone_number, amount, network)


main.add_command(config)
main.add_command(buy_load)

if __name__ == '__main__':
    main()
