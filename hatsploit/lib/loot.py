#!/usr/bin/env python3

#
# MIT License
#
# Copyright (c) 2020-2022 EntySec
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import os
import datetime

from pex.string import String

from hatsploit.core.utils.fs import FSTools
from hatsploit.core.cli.badges import Badges

from hatsploit.lib.config import Config


class Loot(String, FSTools):
    badges = Badges()

    loot = Config().path_config['loot_path']
    data = Config().path_config['data_path']

    def create_loot(self):
        if not os.path.isdir(self.loot):
            os.mkdir(self.loot)

    def specific_loot(self, filename):
        return self.loot + filename

    def random_loot(self, extension=None):
        filename = self.random_string(16)

        if extension:
            filename += '.' + extension

        return self.loot + filename

    def get_file(self, filename):
        if self.exists_file(filename):
            with open(filename, 'rb') as f:
                return f.read()

        return None

    def save_file(self, location, data, extension=None, filename=None):
        exists, is_dir = self.exists(location)

        if exists:
            if is_dir:
                if location.endswith('/'):
                    location += os.path.split(filename)[1] if filename else self.random_string(16)
                else:
                    location += '/' + os.path.split(filename)[1] if filename else self.random_string(16)

            if extension:
                if not location.endswith('.' + extension):
                    location += '.' + extension

            with open(location, 'wb') as f:
                f.write(data)

            self.badges.print_success(f"Saved to {location}!")
            return os.path.abspath(location)

        return None

    def remove_file(self, filename):
        if self.exists_file(filename):
            os.remove(filename)

            self.badges.print_success(f"Removed {filename}!")
            return True

        return False

    def get_loot(self, filename):
        filename = os.path.split(filename)[1]
        return self.get_file(self.loot + filename)

    def save_loot(self, filename, data):
        filename = os.path.split(filename)[1]
        return self.save_file(self.loot + filename, data)

    def remove_loot(self, filename):
        filename = os.path.split(filename)[1]
        return self.remove_file(self.loot + filename)

    def get_data(self, filename):
        if os.path.exists(self.data + filename):
            with open(self.data + filename, 'rb') as f:
                return f.read()
        else:
            self.badges.print_error("Invalid data given!")

    def list_loot(self):
        loots = []

        for loot in os.listdir(self.loot):
            loots.append((loot, self.loot + loot, datetime.datetime.fromtimestamp(
                os.path.getmtime(
                    self.loot + loot
                )).astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")
            ))

        return loots
