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

from hatsploit.core.cli.badges import Badges
from hatsploit.core.db.importer import Importer
from hatsploit.lib.storage import LocalStorage


class Plugins:
    badges = Badges()
    importer = Importer()
    local_storage = LocalStorage()

    def check_exist(self, name):
        all_plugins = self.local_storage.get("plugins")
        if all_plugins:
            for database in all_plugins:
                plugins = all_plugins[database]
                if name in plugins:
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
            for database in all_plugins:
                plugins = all_plugins[database]
                if name in plugins:
                    return database
        return None

    def import_plugin(self, database, plugin):
        loaded_plugins = {}
        plugins = self.local_storage.get("plugins")[database][plugin]
        try:
            loaded_plugins[plugin] = self.importer.import_plugin(plugins['Path'])
        except Exception:
            return None
        return loaded_plugins

    def add_plugin(self, database, plugin):
        plugins = self.local_storage.get("plugins")[database][plugin]

        plugin_object = self.import_plugin(database, plugin)
        if plugin_object:
            if self.local_storage.get("loaded_plugins"):
                self.local_storage.update("loaded_plugins", plugin_object)
            else:
                self.local_storage.set("loaded_plugins", plugin_object)
            self.local_storage.get("loaded_plugins")[plugin].run()
            self.badges.print_success("Successfully loaded " + plugin + " plugin!")
        else:
            self.badges.print_error("Failed to load plugin!")

    def load_plugin(self, plugin):
        plugins_shorts = self.local_storage.get("plugin_shorts")

        if plugins_shorts:
            if plugin.isdigit():
                plugin_number = int(plugin)

                if plugin_number in plugins_shorts:
                    plugin = plugins_shorts[plugin_number]

        self.badges.print_process("Loading " + plugin + " plugin...")

        if not self.check_loaded(plugin):
            if self.check_exist(plugin):
                database = self.get_database(plugin)
                self.add_plugin(database, plugin)
            else:
                self.badges.print_error("Invalid plugin!")
        else:
            self.badges.print_error("Already loaded!")

    def unload_plugin(self, plugin):
        plugins_shorts = self.local_storage.get("plugin_shorts")

        if plugins_shorts:
            if plugin.isdigit():
                plugin_number = int(plugin)

                if plugin_number in plugins_shorts:
                    plugin = plugins_shorts[plugin_number]

        self.badges.print_process("Unloading " + plugin + " plugin...")

        if self.check_loaded(plugin):
            self.local_storage.delete_element("loaded_plugins", plugin)
            self.badges.print_success("Successfully unloaded " + plugin + " plugin!")
        else:
            self.badges.print_error("Plugin not loaded!")
