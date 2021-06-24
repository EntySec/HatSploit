#!/usr/bin/env python3

#
# MIT License
#
# Copyright (c) 2020-2021 EntySec
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

from hatsploit.base.storage import LocalStorage


class Plugins:
    def __init__(self):
        self.local_storage = LocalStorage()

    def check_exist(self, name):
        all_plugins = self.local_storage.get("plugins")
        if all_plugins:
            for database in all_plugins.keys():
                plugins = all_plugins[database]
                if name in plugins.keys():
                    return True
        return False

    def check_loaded(self, name):
        loaded_plugins = self.local_storage.get("loaded_plugins")
        if loaded_plugins:
            if name in loaded_plugins:
                return True
        return False

    def get_database(self, name):
        all_plugins = self.local_storage.get("plugins")
        if all_plugins:
            for database in all_plugins.keys():
                plugins = all_plugins[database]
                if name in plugins.keys():
                    return database
        return None
