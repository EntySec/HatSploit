"""
MIT License

Copyright (c) 2020-2024 EntySec

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

import os
import json

from hatsploit.lib.storage import STORAGE


class DB(object):
    """ Subclass of hatsploit.core.db module.

    This subclass of hatsploit.core.db module is intended for
    providing tools for working with HatSploit databases.
    """

    @staticmethod
    def get_encoder_databases() -> dict:
        """ Get connected encoder databases.

        :return dict: databases, database name as keys and
        database data as items
        """

        return STORAGE.get("connected_encoder_databases", {})

    @staticmethod
    def get_payload_databases() -> dict:
        """ Get connected payload databases.

        :return dict: databases, database name as keys and
        database data as items
        """

        return STORAGE.get("connected_payload_databases", {})

    @staticmethod
    def get_module_databases() -> dict:
        """ Get connected module databases.

        :return dict: databases, database name as keys and
        database data as items
        """

        return STORAGE.get("connected_module_databases", {})

    @staticmethod
    def get_plugin_databases() -> dict:
        """ Get connected plugin databases.

        :return dict: databases, database name as keys and
        database data as items
        """

        return STORAGE.get("connected_plugin_databases", {})

    @staticmethod
    def disconnect_payload_database(name: str) -> None:
        """ Disconnect payload database.

        :param str name: database name
        :return None: None
        :raises RuntimeError: with trailing error message
        """

        if STORAGE.get("connected_payload_databases"):
            if name in STORAGE.get("connected_payload_databases"):
                STORAGE.delete_element("connected_payload_databases", name)
                STORAGE.delete_element("payloads", name)
                return

        raise RuntimeError("No such payload database connected!")

    @staticmethod
    def disconnect_encoder_database(name: str) -> None:
        """ Disconnect encoder database.

        :param str name: database name
        :return None: None
        :raises RuntimeError: with trailing error message
        """

        if STORAGE.get("connected_encoder_databases"):
            if name in STORAGE.get("connected_encoder_databases"):
                STORAGE.delete_element("connected_encoder_databases", name)
                STORAGE.delete_element("encoders", name)
                return

        raise RuntimeError("No such encoder database connected!")

    @staticmethod
    def disconnect_module_database(name: str) -> None:
        """ Disconnect module database.

        :param str name: database name
        :return None: None
        :raises RuntimeError: with trailing error message
        """

        if STORAGE.get("connected_module_databases"):
            if name in STORAGE.get("connected_module_databases"):
                STORAGE.delete_element("connected_module_databases", name)
                STORAGE.delete_element("modules", name)
                return

        raise RuntimeError("No such module database connected!")

    @staticmethod
    def disconnect_plugin_database(name: str) -> None:
        """ Disconnect plugin database.

        :param str name: database name
        :return None: None
        :raises RuntimeError: with trailing error message
        """

        if STORAGE.get("connected_plugin_databases"):
            if name in STORAGE.get("connected_plugin_databases"):
                STORAGE.delete_element("connected_plugin_databases", name)
                STORAGE.delete_element("plugins", name)
                return

        raise RuntimeError("No such plugin database connected!")

    @staticmethod
    def connect_encoder_database(name: str, path: str) -> None:
        """ Connect encoder database.

        :param str name: name to give to the database
        :param str path: path to the database
        :return None: None
        :raises RuntimeError: with trailing error message
        """

        if STORAGE.get("connected_encoder_databases"):
            if name in STORAGE.get("connected_encoder_databases"):
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
        if not STORAGE.get("connected_encoder_databases"):
            STORAGE.set("connected_encoder_databases", {})
        STORAGE.update("connected_encoder_databases", data)

        if STORAGE.get("encoders"):
            STORAGE.update("encoders", encoders)
        else:
            STORAGE.set("encoders", encoders)

    @staticmethod
    def connect_payload_database(name: str, path: str) -> None:
        """ Connect payload database.

        :param str name: name to give to the database
        :param str path: path to the database
        :return None: None
        :raises RuntimeError: with trailing error message
        """

        if STORAGE.get("connected_payload_databases"):
            if name in STORAGE.get("connected_payload_databases"):
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
        if not STORAGE.get("connected_payload_databases"):
            STORAGE.set("connected_payload_databases", {})
        STORAGE.update("connected_payload_databases", data)

        if STORAGE.get("payloads"):
            STORAGE.update("payloads", payloads)
        else:
            STORAGE.set("payloads", payloads)

    @staticmethod
    def connect_module_database(name: str, path: str) -> None:
        """ Connect module database.

        :param str name: name to give to the database
        :param str path: path to the database
        :return None: None
        :raises RuntimeError: with trailing error message
        """

        if STORAGE.get("connected_module_databases"):
            if name in STORAGE.get("connected_module_databases"):
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
        if not STORAGE.get("connected_module_databases"):
            STORAGE.set("connected_module_databases", {})
        STORAGE.update("connected_module_databases", data)

        if STORAGE.get("modules"):
            STORAGE.update("modules", modules)
        else:
            STORAGE.set("modules", modules)

    @staticmethod
    def connect_plugin_database(name: str, path: str) -> None:
        """ Connect plugin database.

        :param str name: name to give to the database
        :param str path: path to the database
        :return None: None
        :raises RuntimeError: with trailing error message
        """

        if STORAGE.get("connected_plugin_databases"):
            if name in STORAGE.get("connected_plugin_databases"):
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
        if not STORAGE.get("connected_plugin_databases"):
            STORAGE.set("connected_plugin_databases", {})
        STORAGE.update("connected_plugin_databases", data)

        if STORAGE.get("plugins"):
            STORAGE.update("plugins", plugins)
        else:
            STORAGE.set("plugins", plugins)
