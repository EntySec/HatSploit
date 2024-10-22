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

import sys
import traceback

from typing import Union

from hatsploit.lib.core.plugin import Plugin

from hatsploit.core.db.db import DB

from hatsploit.lib.storage import STORAGE


class Plugins(object):
    """ Subclass of hatsploit.lib module.

    This subclass of hatsploit.lib module is intended for providing
    tools for working with HatSploit plugins.
    """

    def plugins_completer(self) -> list:
        """ Tab-completion for plugins.

        :return list: list of completions
        """

        return {plugin: None for plugin in self.get_plugins()}

    @staticmethod
    def get_plugins(criteria: dict = {}, query: dict = {}) -> dict:
        """ Get all plugins from local storage.

        :param dict criteria: DB search criteria
        :param dict query: plugin search query
        :return dict: plugins, plugin names as keys and
        plugin objects as items
        """

        return DB(table='plugins').dump(
            criteria=criteria, query=query)

    @staticmethod
    def get_loaded_plugins() -> dict:
        """ Get all loaded plugins from local storage.

        :return dict: plugins, plugin name as keys and
        plugin objects as items
        """

        return STORAGE.get("loaded_plugins", {})

    def loaded_plugins_completer(self) -> list:
        """ Tab-completion for loaded plugins
        (used for auto-completing 'unload' command).

        :return list: list of completions
        """

        return {plugin: None for plugin in self.get_loaded_plugins()}

    def check_exist(self, plugin: str) -> bool:
        """ Check if plugin exists in the database.

        :param str plugin: payload name
        :return bool: True if exists else False
        """

        return plugin in self.get_plugins()

    def check_loaded(self, plugin: str) -> bool:
        """ Check if plugin is loaded.

        :param str plugin: plugin name
        :return bool: True if loaded else False
        """

        return plugin in self.get_loaded_plugins()

    @staticmethod
    def import_plugin(plugin: str) -> Union[Plugin, None]:
        """ Import plugin.

        :param str plugin: plugin name
        :return Union[Plugin, None]: imported plugin, None if failed to import
        """

        try:
            plugin_object = DB(table='plugins').load(
                criteria={'BaseName': plugin}).get(plugin)

        except Exception:
            traceback.print_exc(file=sys.stdout)
            return

        return plugin_object

    def add_plugin(self, plugin: str) -> Union[Plugin, None]:
        """ Add plugin.

        :param str plugin: plugin name
        :return None: None
        :raises RuntimeError: with trailing error message
        """

        plugin_object = self.import_plugin(plugin)

        if plugin_object:
            if self.get_loaded_plugins():
                STORAGE.update("loaded_plugins", {plugin: plugin_object})
            else:
                STORAGE.set("loaded_plugins", {plugin: plugin_object})

            plugin_object.load()
            return plugin_object
        else:
            raise RuntimeError(f"Failed to load plugin: {plugin}!")

    def load_plugin(self, plugin: str) -> Union[Plugin, None]:
        """ Load specific plugin.

        :param str plugin: plugin name or number
        :return None: None
        :raises RuntimeError: with trailing error message
        """

        plugin_shorts = STORAGE.get("plugin_shorts")

        if plugin_shorts:
            if plugin.isdigit():
                plugin_number = int(plugin)

                if plugin_number in plugin_shorts:
                    plugin = plugin_shorts[plugin_number]

        if not self.check_loaded(plugin):
            if self.check_exist(plugin):
                return self.add_plugin(plugin)

            else:
                raise RuntimeError(f"Invalid plugin: {plugin}!")
        else:
            raise RuntimeWarning(f"Plugin is already loaded: {plugin}.")

    def unload_plugin(self, plugin: str) -> None:
        """ Unload specific loaded plugin.

        :param str plugin: plugin name or number
        :return None: None
        :raises RuntimeError: with trailing error message
        """

        plugin_shorts = STORAGE.get("plugin_shorts")

        if plugin_shorts:
            if plugin.isdigit():
                plugin_number = int(plugin)

                if plugin_number in plugin_shorts:
                    plugin = plugin_shorts[plugin_number]

        if self.check_loaded(plugin):
            plugin_object = self.get_loaded_plugins()[plugin]
            plugin_object.unload()

            STORAGE.delete_element("loaded_plugins", plugin)

        else:
            raise RuntimeError(f"Plugin is not loaded: {plugin}!")
