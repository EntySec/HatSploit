#!/usr/bin/env python3

#
# This command requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.lib.storage import LocalStorage
from hatsploit.core.db.importer import Importer
from hatsploit.lib.command import Command
from hatsploit.lib.plugins import Plugins


class HatSploitCommand(Command):
    plugins = Plugins()
    local_storage = LocalStorage()
    importer = Importer()

    details = {
        'Category': "plugins",
        'Name': "load",
        'Authors': [
            'Ivan Nikolsky (enty8080) - command developer'
        ],
        'Description': "Load specified plugin.",
        'Usage': "load <plugin>",
        'MinArgs': 1
    }

    def import_plugin(self, database, plugin):
        loaded_plugins = dict()
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
            self.print_success("Successfully loaded " + plugin + " plugin!")
        else:
            self.print_error("Failed to load plugin!")

    def run(self, argc, argv):
        plugin = argv[0]
        self.print_process("Loading " + plugin + " plugin...")

        if not self.plugins.check_loaded(plugin):
            if self.plugins.check_exist(plugin):
                database = self.plugins.get_database(plugin)
                self.add_plugin(database, plugin)
            else:
                self.print_error("Invalid plugin!")
        else:
            self.print_error("Already loaded!")
