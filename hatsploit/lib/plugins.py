"""
MIT License

Copyright (c) 2020-2023 EntySec

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

from typing import Union

from hatsploit.lib.plugin import Plugin

from hatsploit.core.db.importer import Importer
from hatsploit.lib.storage import LocalStorage


class Plugins(object):
    """ Subclass of hatsploit.lib module.

    This subclass of hatsploit.lib module is intended for providing
    tools for working with HatSploit plugins.
    """

    def __init__(self) -> None:
        super().__init__()

        self.importer = Importer()
        self.local_storage = LocalStorage()

    def plugins_completer(self, text: str) -> list:
        """ Tab-completion for plugins.

        :param str text: text to complete
        :return list: list of completions
        """

        plugins = self.get_plugins()
        matches = []

        if plugins:
            for database in plugins:
                for plugin in plugins[database]:
                    if plugin.startswith(text):
                        matches.append(plugin)

        return matches

    def get_plugins(self) -> dict:
        """ Get all plugins from local storage.

        :return dict: plugins, plugin names as keys and
        plugin objects as items
        """

        return self.local_storage.get("plugins")

    def get_loaded_plugins(self) -> dict:
        """ Get all loaded plugins from local storage.

        :return dict: plugins, plugin name as keys and
        plugin objects as items
        """

        return self.local_storage.get("loaded_plugins")

    def loaded_plugins_completer(self, text: str) -> list:
        """ Tab-completion for loaded plugins
        (used for auto-completing 'unload' command).

        :param str text: text to complete
        :return list: list of completions
        """

        plugins = self.get_loaded_plugins()

        if plugins:
            return [plugin for plugin in plugins if plugin.startswith(text)]

        return []

    def check_exist(self, plugin: str) -> bool:
        """ Check if plugin exists in the database.

        :param str plugin: payload name
        :return bool: True if exists else False
        """

        all_plugins = self.get_plugins()

        if all_plugins:
            for database in all_plugins:
                plugins = all_plugins[database]

                if plugin in plugins:
                    return True

        return False

    def check_loaded(self, plugin: str) -> bool:
        """ Check if plugin is loaded.

        :param str plugin: plugin name
        :return bool: True if loaded else False
        """

        loaded_plugins = self.get_loaded_plugins()

        if loaded_plugins:
            if plugin in loaded_plugins:
                return True

        return False

    def get_database(self, plugin: str) -> str:
        """ Get database in which specific plugin exists.

        :param str plugin: plugin name
        :return str: database name
        """

        all_plugins = self.get_plugins()

        if all_plugins:
            for database in all_plugins:
                plugins = all_plugins[database]

                if plugin in plugins:
                    return database

        return ''

    def import_plugin(self, database: str, plugin: str) -> Union[Plugin, None]:
        """ Import plugin.

        :param str database: database name
        :param str plugin: plugin name
        :return Union[Plugin, None]: imported plugin, None if failed to import
        """

        loaded_plugins = {}
        plugins = self.get_plugins()[database][plugin]

        try:
            plugin_object = self.importer.import_plugin(plugins['Path'])
            loaded_plugins[plugin] = plugin_object

            return plugin_object

        except Exception:
            pass

    def import_plugins(self, path: str) -> dict:
        """ Import plugins from path.

        :param str path: path to plugins
        :return dict: plugins, plugin names as keys and
        plugin objects as items
        """

        return self.importer.import_plugins(path)

    def add_plugin(self, database: str, plugin: str) -> None:
        """ Add plugin.

        :param str database: database name
        :param str plugin: plugin name
        :return None: None
        :raises RuntimeError: with trailing error message
        """

        plugin_object = self.import_plugin(database, plugin)

        if plugin_object:
            if self.get_loaded_plugins():
                self.local_storage.update("loaded_plugins", {plugin: plugin_object})
            else:
                self.local_storage.set("loaded_plugins", {plugin: plugin_object})

            self.get_loaded_plugins()[plugin].load()
        else:
            raise RuntimeError(f"Failed to load plugin: {plugin}!")

    def load_plugin(self, plugin: str) -> None:
        """ Load specific plugin.

        :param str plugin: plugin name or number
        :return None: None
        :raises RuntimeError: with trailing error message
        """

        plugin_shorts = self.local_storage.get("plugin_shorts")

        if plugin_shorts:
            if plugin.isdigit():
                plugin_number = int(plugin)

                if plugin_number in plugin_shorts:
                    plugin = plugin_shorts[plugin_number]

        if not self.check_loaded(plugin):
            if self.check_exist(plugin):
                database = self.get_database(plugin)
                self.add_plugin(database, plugin)

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

        plugin_shorts = self.local_storage.get("plugin_shorts")

        if plugin_shorts:
            if plugin.isdigit():
                plugin_number = int(plugin)

                if plugin_number in plugin_shorts:
                    plugin = plugin_shorts[plugin_number]

        if self.check_loaded(plugin):
            self.local_storage.delete_element("loaded_plugins", plugin)

        else:
            raise RuntimeError(f"Plugin is not loaded: {plugin}!")
