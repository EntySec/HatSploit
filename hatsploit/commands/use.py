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
        'Category': "module",
        'Name': "use",
        'Authors': [
            'Ivan Nikolsky (enty8080)'
        ],
        'Description': "Use specified module.",
        'Usage': "use <module>",
        'MinArgs': 1
    }

    def check_if_already_used(self, module):
        if self.modules.check_current_module():
            if module == self.modules.get_current_module_name():
                return True
        return False

    def run(self, argc, argv):
        module = argv[0]

        if not self.check_if_already_used(module):
            if self.modules.check_exist(module):
                self.modules.add_module(module)
            else:
                self.output_error("Invalid module!")
