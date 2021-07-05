#!/usr/bin/env python3

#
# This command requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

import os

from hatsploit.lib.storage import LocalStorage
from hatsploit.lib.config import Config
from hatsploit.lib.command import Command
from hatsploit.lib.modules import Modules
from hatsploit.core.base.execute import Execute


class HatSploitCommand(Command):
    config = Config()
    modules = Modules()
    local_storage = LocalStorage()
    execute = Execute()

    details = {
        'Category': "developer",
        'Name': "edit",
        'Authors': [
            'Ivan Nikolsky (enty8080) - command developer'
        ],
        'Description': "Open module in editor.",
        'Usage': "edit <module>",
        'MinArgs': 1
    }

    def run(self, argc, argv):
        module = argv[0]

        try:
            if not os.environ['EDITOR']:
                self.output_warning("Shell variable EDITOR not set.")
                editor = "vi"
            else:
                editor = os.environ['EDITOR']
        except KeyError:
            self.output_warning("Shell variable EDITOR not set.")
            editor = "vi"

        if self.modules.check_exist(module):
            if not self.modules.check_imported(module):
                database = self.modules.get_database(module)
                module_path = self.local_storage.get(
                    "modules"
                )[database][module]['Path']
                edit_mode = editor + " " + self.config.path_config['root_path'] + module_path
                self.execute.execute_system(edit_mode)
            else:
                self.output_error("Can not edit already used module!")
        else:
            self.output_error("Invalid module!")
