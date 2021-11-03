#!/usr/bin/env python3

#
# This command requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.lib.command import Command
from hatsploit.lib.plugins import Plugins
from hatsploit.lib.storage import LocalStorage


class HatSploitCommand(Command):
    local_storage = LocalStorage()
    plugins = Plugins()

    details = {
        'Category': "plugins",
        'Name': "unload",
        'Authors': [
            'Ivan Nikolsky (enty8080) - command developer'
        ],
        'Description': "Unload specified loaded plugin.",
        'Usage': "unload <plugin>",
        'MinArgs': 1
    }

    def run(self, argc, argv):
        plugin = argv[1]
        self.print_process("Unloading " + plugin + " plugin...")

        if self.plugins.check_loaded(plugin):
            self.local_storage.delete_element("loaded_plugins", plugin)
            self.print_success("Successfully unloaded " + plugin + " plugin!")
        else:
            self.print_error("Plugin not loaded!")
