#!/usr/bin/env python3

#
# This command requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

import os

from hatsploit.core.base.storage import LocalStorage
from hatsploit.core.base.config import Config
from hatsploit.command import Command
from hatsploit.core.modules.modules import Modules


class HatSploitCommand(Command):
    config = Config()
    modules = Modules()
    local_storage = LocalStorage()

    details = {
        'Category': "developer",
        'Name': "edit",
        'Authors': [
            'Ivan Nikolsky (enty8080)'
        ],
        'Description': "Open module in editor.",
        'Usage': "edit <module>",
        'MinArgs': 1
    }

    def run(self, argc, argv):
        module = argv[0]

        module_category = self.modules.get_category(module)
        module_platform = self.modules.get_platform(module)
        module_name = self.modules.get_name(module)

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
                )[database][module_category][module_platform][module_name]['Path']
                edit_mode = editor + " " + self.config.path_config['root_path'] + module_path
                self.execute.execute_system(edit_mode)
            else:
                self.output_error("Can not edit already used module!")
        else:
            self.output_error("Invalid module!")
