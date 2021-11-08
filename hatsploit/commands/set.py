#!/usr/bin/env python3

#
# This command requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.lib.command import Command
from hatsploit.lib.modules import Modules


class HatSploitCommand(Command):
    modules = Modules()

    details = {
        'Category': "modules",
        'Name': "set",
        'Authors': [
            'Ivan Nikolsky (enty8080) - command developer'
        ],
        'Description': "Set an option value.",
        'Usage': "set <option> <value>",
        'MinArgs': 2
    }

    def run(self, argc, argv):
        self.modules.set_current_module_option(argv[1].upper(), argv[2])
