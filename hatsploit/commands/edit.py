#!/usr/bin/env python3

#
# This command requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

import os

from hatsploit.core.base.execute import Execute

from hatsploit.lib.command import Command
from hatsploit.lib.modules import Modules


class HatSploitCommand(Command):
    modules = Modules()
    execute = Execute()

    details = {
        'Category': "modules",
        'Name': "edit",
        'Authors': [
            'Ivan Nikolsky (enty8080) - command developer'
        ],
        'Description': "Open module in editor.",
        'Usage': "edit <module>",
        'MinArgs': 1
    }

    complete = modules.modules_completer

    def run(self, argc, argv):
        module = argv[1]

        try:
            if not os.environ['EDITOR']:
                self.print_warning("Shell variable EDITOR not set.")
                editor = "vi"
            else:
                editor = os.environ['EDITOR']
        except KeyError:
            self.print_warning("Shell variable EDITOR not set.")
            editor = "vi"

        if self.modules.check_exist(module):
            if not self.modules.check_imported(module):
                database = self.modules.get_database(module)
                module_path = self.modules.get_modules()[database][module]['Path']

                edit_mode = editor + ' ' + module_path + '.py'
                self.execute.execute_system(self.format_commands(edit_mode))
            else:
                self.print_error("Can not edit already used module!")
        else:
            self.print_error("Invalid module!")
