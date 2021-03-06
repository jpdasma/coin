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
from setuptools import setup, find_packages


with open('LICENSE') as f:
    license = f.read()

setup(
    name='coin',
    version='0.1.0',
    description='A command line tool for coins.ph',
    author='Julian Paul Dasmariñas',
    author_email='julian.dasma@gmail.com',
    url='https://github.com/jpdasma/coin',
    license=license,
    packages=find_packages(exclude=('tests')),
    entry_points={
        'console_scripts': ['coin-cmd=coin.command_line:main'],
    }
)
