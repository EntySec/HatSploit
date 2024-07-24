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

import importlib.util

from typing import Union
from badges import Badges

from hatsploit.core.db.db import DB
from hatsploit.lib.config import Config

from hatsploit.lib.core.module import Module
from hatsploit.lib.core.plugin import Plugin
from hatsploit.lib.core.encoder import Encoder
from hatsploit.lib.core.payload import Payload

from hatsploit.lib.storage import STORAGE


class Importer(Config, Badges, DB):
    """ Subclass of hatsploit.core.db module.

    This subclass of hatsploit.core.db module is intended for
    providing tools for importing HatSploit modules, plugins,
    commands, etc.
    """

    @staticmethod
    def import_payload(payload_path: str) -> Payload:
        """ Import payload from path.

        :param str payload_path: path to payload
        :return Payload: payload object
        :raises RuntimeError: with trailing error message
        """

        try:
            if not payload_path.endswith('.py'):
                payload_path = payload_path + '.py'

            spec = importlib.util.spec_from_file_location(payload_path, payload_path)
            payload = importlib.util.module_from_spec(spec)

            spec.loader.exec_module(payload)
            payload = payload.HatSploitPayload()

        except Exception as e:
            raise RuntimeError(f"Failed to import payload: {str(e)}!")

        return payload

    @staticmethod
    def import_encoder(encoder_path: str) -> Encoder:
        """ Import encoder from path.

        :param str encoder_path: path to encoder
        :return Encoder: encoder object
        :raises RuntimeError: with trailing error message
        """

        try:
            if not encoder_path.endswith('.py'):
                encoder_path = encoder_path + '.py'

            spec = importlib.util.spec_from_file_location(encoder_path, encoder_path)
            encoder = importlib.util.module_from_spec(spec)

            spec.loader.exec_module(encoder)
            encoder = encoder.HatSploitEncoder()

        except Exception as e:
            raise RuntimeError(f"Failed to import encoder: {str(e)}!")

        return encoder

    @staticmethod
    def import_module(module_path: str) -> Module:
        """ Import module from path.

        :param str module_path: path to module
        :return Module: module object
        :raises RuntimeError: with trailing error message
        """

        try:
            if not module_path.endswith('.py'):
                module_path = module_path + '.py'

            spec = importlib.util.spec_from_file_location(module_path, module_path)
            module = importlib.util.module_from_spec(spec)

            spec.loader.exec_module(module)
            module = module.HatSploitModule()

        except Exception as e:
            raise RuntimeError(f"Failed to import module: {str(e)}!")

        return module

    @staticmethod
    def import_plugin(plugin_path: str) -> Plugin:
        """ Import plugin from path.

        :param str plugin_path: path to plugin
        :return Plugin: plugin object
        :raises RuntimeError: with trailing error message
        """

        try:
            if not plugin_path.endswith('.py'):
                plugin_path = plugin_path + '.py'

            spec = importlib.util.spec_from_file_location(plugin_path, plugin_path)
            plugin = importlib.util.module_from_spec(spec)

            spec.loader.exec_module(plugin)
            plugin = plugin.HatSploitPlugin()

        except Exception as e:
            raise RuntimeError(f"Failed to import plugin: {str(e)}!")

        return plugin

    def import_plugins(self, path: str) -> dict:
        """ Import all plugins from path.

        :param str path: path to plguins
        :return dict: plugins, plugin names as keys and
        plugin objects as items
        """

        if not path.endswith('/'):
            path += '/'

        plugins = {}
        plugin_path = os.path.split(path)[0]

        for file in os.listdir(plugin_path):
            if not file.endswith('py'):
                continue

            try:
                plugin_object = self.import_plugin(plugin_path + '/' + file[:-3])
                plugin_name = plugin_object.info['Plugin']
                plugins[plugin_name] = plugin_object

            except Exception as e:
                self.print_error(f"Failed to load {file[:-3]} plugin!")
                self.print_error(str(e))

        return plugins

    def import_base_databases(self) -> None:
        """ Import base databases.

        :return None: None
        """

        base_dbs = self.db_config['base_dbs']
        db_path = self.path_config['db_path']

        if os.path.exists(db_path + base_dbs['module_database']):
            self.connect_module_database(
                base_dbs['module_database_name'],
                db_path + base_dbs['module_database'],
            )

        if os.path.exists(db_path + base_dbs['payload_database']):
            self.connect_payload_database(
                base_dbs['payload_database_name'],
                db_path + base_dbs['payload_database'],
            )

        if os.path.exists(db_path + base_dbs['encoder_database']):
            self.connect_encoder_database(
                base_dbs['encoder_database_name'],
                db_path + base_dbs['encoder_database'],
            )

        if os.path.exists(db_path + base_dbs['plugin_database']):
            self.connect_plugin_database(
                base_dbs['plugin_database_name'],
                db_path + base_dbs['plugin_database'],
            )

    def import_all(self) -> None:
        """ Import all base commands and all base databases.

        :return None: None
        """

        self.import_base_databases()
