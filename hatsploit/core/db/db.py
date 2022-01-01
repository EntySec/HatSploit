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

import json
import os

from hatsploit.core.cli.badges import Badges
from hatsploit.lib.config import Config
from hatsploit.lib.storage import LocalStorage


class DB:
    badges = Badges()
    config = Config()
    local_storage = LocalStorage()

    def disconnect_payload_database(self, name):
        if self.local_storage.get("connected_payload_databases"):
            if name in self.local_storage.get("connected_payload_databases"):
                self.local_storage.delete_element("connected_payload_databases", name)
                self.local_storage.delete_element("payloads", name)
                return
        self.badges.print_error("No such payload database connected!")

    def disconnect_module_database(self, name):
        if self.local_storage.get("connected_module_databases"):
            if name in self.local_storage.get("connected_module_databases"):
                self.local_storage.delete_element("connected_module_databases", name)
                self.local_storage.delete_element("modules", name)
                return
        self.badges.print_error("No such module database connected!")

    def disconnect_plugin_database(self, name):
        if self.local_storage.get("connected_plugin_databases"):
            if name in self.local_storage.get("connected_plugin_databases"):
                self.local_storage.delete_element("connected_plugin_databases", name)
                self.local_storage.delete_element("plugins", name)
                return
        self.badges.print_error("No such plugin database connected!")

    def connect_payload_database(self, name, path):
        if self.local_storage.get("connected_payload_databases"):
            if name in self.local_storage.get("connected_payload_databases"):
                self.badges.print_error("Payload database already connected!")
                return
        if not os.path.exists(path) or not str.endswith(path, "json"):
            self.badges.print_error("Not a payload database!")
            return

        try:
            database = json.load(open(path))
        except Exception:
            self.badges.print_error("Failed to connect payload database!")
            return

        if '__database__' not in database:
            self.badges.print_error("No __database__ section found!")
            return
        if database['__database__']['type'] != "payloads":
            self.badges.print_error("Not a payload database!")
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
        if not self.local_storage.get("connected_payload_databases"):
            self.local_storage.set("connected_payload_databases", {})
        self.local_storage.update("connected_payload_databases", data)

        if self.local_storage.get("payloads"):
            self.local_storage.update("payloads", payloads)
        else:
            self.local_storage.set("payloads", payloads)

    def connect_module_database(self, name, path):
        if self.local_storage.get("connected_module_databases"):
            if name in self.local_storage.get("connected_module_databases"):
                self.badges.print_error("Module database already connected!")
                return
        if not os.path.exists(path) or not str.endswith(path, "json"):
            self.badges.print_error("Not a module database!")
            return

        try:
            database = json.load(open(path))
        except Exception:
            self.badges.print_error("Failed to connect module database!")
            return

        if '__database__' not in database:
            self.badges.print_error("No __database__ section found!")
            return
        if database['__database__']['type'] != "modules":
            self.badges.print_error("Not a module database!")
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
        if not self.local_storage.get("connected_module_databases"):
            self.local_storage.set("connected_module_databases", {})
        self.local_storage.update("connected_module_databases", data)

        if self.local_storage.get("modules"):
            self.local_storage.update("modules", modules)
        else:
            self.local_storage.set("modules", modules)

    def connect_plugin_database(self, name, path):
        if self.local_storage.get("connected_plugin_databases"):
            if name in self.local_storage.get("connected_plugin_databases"):
                self.badges.print_error("Plugin database already connected!")
                return
        if not os.path.exists(path) or not str.endswith(path, "json"):
            self.badges.print_error("Not a database!")
            return

        try:
            database = json.load(open(path))
        except Exception:
            self.badges.print_error("Failed to connect plugin database!")
            return

        if '__database__' not in database:
            self.badges.print_error("No __database__ section found!")
            return
        if database['__database__']['type'] != "plugins":
            self.badges.print_error("Not a plugin database!")
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
        if not self.local_storage.get("connected_plugin_databases"):
            self.local_storage.set("connected_plugin_databases", {})
        self.local_storage.update("connected_plugin_databases", data)

        if self.local_storage.get("plugins"):
            self.local_storage.update("plugins", plugins)
        else:
            self.local_storage.set("plugins", plugins)
