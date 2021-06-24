#!/usr/bin/env python3

#
# This command requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.base.storage import LocalStorage
from hatsploit.base.command import Command
from hatsploit.base.plugins import Plugins


class HatSploitCommand(Command):
    local_storage = LocalStorage()
    plugins = Plugins()

    details = {
        'Category': "plugin",
        'Name': "unload",
        'Authors': [
            'Ivan Nikolsky (enty8080)'
        ],
        'Description': "Unload specified loaded plugin.",
        'Usage': "unload <plugin>",
        'MinArgs': 1
    }

    def run(self, argc, argv):
        plugin = argv[0]
        self.output_process("Unloading " + plugin + " plugin...")

        if self.plugins.check_loaded(plugin):
            self.local_storage.delete_element("loaded_plugins", plugin)
            self.output_success("Successfully unloaded " + plugin + " plugin!")
        else:
            self.output_error("Plugin not loaded!")
