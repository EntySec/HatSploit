#!/usr/bin/env python3

#
# This command requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.command import Command

from hatsploit.core.modules.modules import Modules


class HatSploitCommand(Command):
    modules = Modules()

    details = {
        'Category': "module",
        'Name': "set",
        'Authors': [
            'Ivan Nikolsky (enty8080)'
        ],
        'Description': "Set an option value.",
        'Usage': "set <option> <value>",
        'MinArgs': 2
    }

    def run(self, argc, argv):
        option = argv[0].upper()
        value = argv[1]

        self.modules.set_current_module_option(option, value)
