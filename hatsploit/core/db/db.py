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

import json
import os

from hatsploit.base.config import Config
from hatsploit.base.storage import LocalStorage
from hatsploit.core.cli.badges import Badges


class DB:
    def __init__(self):
        self.badges = Badges()
        self.config = Config()
        self.local_storage = LocalStorage()

    def disconnect_payloads_database(self, name):
        if self.local_storage.get("connected_payloads_databases"):
            if name in self.local_storage.get("connected_payloads_databases"):
                self.local_storage.delete_element("connected_payloads_databases", name)
                self.local_storage.delete_element("payloads", name)
                return
        self.badges.output_error("No such payloads database connected!")

    def disconnect_modules_database(self, name):
        if self.local_storage.get("connected_modules_databases"):
            if name in self.local_storage.get("connected_modules_databases"):
                self.local_storage.delete_element("connected_modules_databases", name)
                self.local_storage.delete_element("modules", name)
                return
        self.badges.output_error("No such modules database connected!")

    def disconnect_plugins_database(self, name):
        if self.local_storage.get("connected_plugins_databases"):
            if name in self.local_storage.get("connected_plugins_databases"):
                self.local_storage.delete_element("connected_plugins_databases", name)
                self.local_storage.delete_element("plugins", name)
                return
        self.badges.output_error("No such plugins database connected!")

    def connect_payloads_database(self, name, path):
        if self.local_storage.get("connected_payloads_databases"):
            if name in self.local_storage.get("connected_payloads_databases"):
                self.bagdes.output_error("Payloads database already connected!")
                return
        if not os.path.exists(path) or not str.endswith(path, "json"):
            self.badges.output_error("Not a payloads database!")
            return

        try:
            database = json.load(open(path))
        except Exception:
            self.badges.output_error("Failed to connect payloads database!")
            return

        if '__database__' not in database.keys():
            self.badges.output_error("No __database__ section found!")
            return
        if database['__database__']['type'] != "payloads":
            self.badges.output_error("Not a payloads database!")
            return
        del database['__database__']

        payloads = {
            name: database
        }

        data = {
            name: {
                'path': path
            }
        }
        if not self.local_storage.get("connected_payloads_databases"):
            self.local_storage.set("connected_payloads_databases", dict())
        self.local_storage.update("connected_payloads_databases", data)

        if self.local_storage.get("payloads"):
            self.local_storage.update("payloads", payloads)
        else:
            self.local_storage.set("payloads", payloads)

    def connect_modules_database(self, name, path):
        if self.local_storage.get("connected_modules_databases"):
            if name in self.local_storage.get("connected_modules_databases"):
                self.bagdes.output_error("Modules database already connected!")
                return
        if not os.path.exists(path) or not str.endswith(path, "json"):
            self.badges.output_error("Not a modules database!")
            return

        try:
            database = json.load(open(path))
        except Exception:
            self.badges.output_error("Failed to connect modules database!")
            return

        if '__database__' not in database.keys():
            self.badges.output_error("No __database__ section found!")
            return
        if database['__database__']['type'] != "modules":
            self.badges.output_error("Not a modules database!")
            return
        del database['__database__']

        modules = {
            name: database
        }

        data = {
            name: {
                'path': path
            }
        }
        if not self.local_storage.get("connected_modules_databases"):
            self.local_storage.set("connected_modules_databases", dict())
        self.local_storage.update("connected_modules_databases", data)

        if self.local_storage.get("modules"):
            self.local_storage.update("modules", modules)
        else:
            self.local_storage.set("modules", modules)

    def connect_plugins_database(self, name, path):
        if self.local_storage.get("connected_plugins_databases"):
            if name in self.local_storage.get("connected_plugins_databases"):
                self.bagdes.output_error("Plugins database already connected!")
                return
        if not os.path.exists(path) or not str.endswith(path, "json"):
            self.badges.output_error("Not a database!")
            return

        try:
            database = json.load(open(path))
        except Exception:
            self.badges.output_error("Failed to connect plugins database!")
            return

        if '__database__' not in database.keys():
            self.badges.output_error("No __database__ section found!")
            return
        if database['__database__']['type'] != "plugins":
            self.badges.output_error("Not a plugins database!")
            return
        del database['__database__']

        plugins = {
            name: database
        }

        data = {
            name: {
                'path': path
            }
        }
        if not self.local_storage.get("connected_plugins_databases"):
            self.local_storage.set("connected_plugins_databases", dict())
        self.local_storage.update("connected_plugins_databases", data)

        if self.local_storage.get("plugins"):
            self.local_storage.update("plugins", plugins)
        else:
            self.local_storage.set("plugins", plugins)
