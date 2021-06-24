#!/usr/bin/env python3

#
# This command requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.base.storage import LocalStorage
from hatsploit.core.db.importer import Importer
from hatsploit.base.command import Command
from hatsploit.base.modules import Modules


class HatSploitCommand(Command):
    importer = Importer()
    local_storage = LocalStorage()
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

        category = self.modules.get_category(module)
        platform = self.modules.get_platform(module)
        name = self.modules.get_name(module)

        if not self.check_if_already_used(module):
            if self.modules.check_exist(module):
                self.modules.add_module(category, platform, name)
            else:
                self.output_error("Invalid module!")
