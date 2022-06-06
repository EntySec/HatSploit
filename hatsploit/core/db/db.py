"""
MIT License

Copyright (c) 2020-2022 EntySec

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import json
import os

from hatsploit.lib.storage import LocalStorage


class DB:
    local_storage = LocalStorage()

    def disconnect_payload_database(self, name):
        if self.local_storage.get("connected_payload_databases"):
            if name in self.local_storage.get("connected_payload_databases"):
                self.local_storage.delete_element("connected_payload_databases", name)
                self.local_storage.delete_element("payloads", name)
                return

        raise RuntimeError("No such payload database connected!")

    def disconnect_encoder_database(self, name):
        if self.local_storage.get("connected_encoder_databases"):
            if name in self.local_storage.get("connected_encoder_databases"):
                self.local_storage.delete_element("connected_encoder_databases", name)
                self.local_storage.delete_element("encoders", name)
                return

        raise RuntimeError("No such encoder database connected!")

    def disconnect_module_database(self, name):
        if self.local_storage.get("connected_module_databases"):
            if name in self.local_storage.get("connected_module_databases"):
                self.local_storage.delete_element("connected_module_databases", name)
                self.local_storage.delete_element("modules", name)
                return

        raise RuntimeError("No such module database connected!")

    def disconnect_plugin_database(self, name):
        if self.local_storage.get("connected_plugin_databases"):
            if name in self.local_storage.get("connected_plugin_databases"):
                self.local_storage.delete_element("connected_plugin_databases", name)
                self.local_storage.delete_element("plugins", name)
                return

        raise RuntimeError("No such plugin database connected!")

    def connect_encoder_database(self, name, path):
        if self.local_storage.get("connected_encoder_databases"):
            if name in self.local_storage.get("connected_encoder_databases"):
                raise RuntimeWarning(f"Encoder database is already connected: {path}.")

        if not os.path.exists(path) or not str.endswith(path, "json"):
            raise RuntimeError(f"Not an encoder database: {path}!")

        try:
            database = json.load(open(path))
        except Exception:
            raise RuntimeError(f"Failed to connect encoder database: {path}!")

        if '__database__' not in database:
            raise RuntimeError(f"No __database__ section found in database: {path}!")

        if database['__database__']['Type'] != "encoders":
            raise RuntimeError(f"Not an encoder database: {path}!")

        del database['__database__']

        encoders = {name: database}

        data = {name: {'Path': path}}
        if not self.local_storage.get("connected_encoder_databases"):
            self.local_storage.set("connected_encoder_databases", {})
        self.local_storage.update("connected_encoder_databases", data)

        if self.local_storage.get("encoders"):
            self.local_storage.update("encoders", encoders)
        else:
            self.local_storage.set("encoders", encoders)

    def connect_payload_database(self, name, path):
        if self.local_storage.get("connected_payload_databases"):
            if name in self.local_storage.get("connected_payload_databases"):
                raise RuntimeWarning(f"Payload database is already connected: {path}.")

        if not os.path.exists(path) or not str.endswith(path, "json"):
            raise RuntimeError(f"Not a payload database: {path}!")

        try:
            database = json.load(open(path))
        except Exception:
            raise RuntimeError(f"Failed to connect payload database: {path}!")

        if '__database__' not in database:
            raise RuntimeError(f"No __database__ section found in database: {path}!")

        if database['__database__']['Type'] != "payloads":
            raise RuntimeError(f"Not a payload database: {path}!")

        del database['__database__']

        payloads = {name: database}

        data = {name: {'Path': path}}
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
                raise RuntimeWarning(f"Module database is already connected: {path}.")

        if not os.path.exists(path) or not str.endswith(path, "json"):
            raise RuntimeError(f"Not a module database: {path}!")

        try:
            database = json.load(open(path))
        except Exception:
            raise RuntimeError(f"Failed to connect module database: {path}!")

        if '__database__' not in database:
            raise RuntimeError(f"No __database__ section found in database: {path}!")

        if database['__database__']['Type'] != "modules":
            raise RuntimeError(f"Not a module database: {path}!")

        del database['__database__']

        modules = {name: database}

        data = {name: {'Path': path}}
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
                raise RuntimeWarning(f"Plugin database is already connected: {path}.")

        if not os.path.exists(path) or not str.endswith(path, "json"):
            raise RuntimeError(f"Not a plugin database: {path}!")

        try:
            database = json.load(open(path))
        except Exception:
            raise RuntimeError(f"Failed to connect plugin database: {path}!")

        if '__database__' not in database:
            raise RuntimeError(f"No __database__ section found in database: {path}!")

        if database['__database__']['Type'] != "plugins":
            raise RuntimeError(f"Not a plugin database: {path}!")

        del database['__database__']

        plugins = {name: database}

        data = {name: {'Path': path}}
        if not self.local_storage.get("connected_plugin_databases"):
            self.local_storage.set("connected_plugin_databases", {})
        self.local_storage.update("connected_plugin_databases", data)

        if self.local_storage.get("plugins"):
            self.local_storage.update("plugins", plugins)
        else:
            self.local_storage.set("plugins", plugins)
