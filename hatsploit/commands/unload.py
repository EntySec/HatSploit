#!/usr/bin/env python3

#
# This command requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.lib.command import Command
from hatsploit.lib.plugins import Plugins


class HatSploitCommand(Command):
    plugins = Plugins()

    details = {
        'Category': "plugins",
        'Name': "unload",
        'Authors': [
            'Ivan Nikolsky (enty8080) - command developer'
        ],
        'Description': "Unload specified loaded plugin.",
        'Usage': "unload <plugin|number>",
        'MinArgs': 1
    }

    def run(self, argc, argv):
        self.plugins.unload_plugin(argv[1])
