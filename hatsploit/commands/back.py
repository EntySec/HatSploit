#!/usr/bin/env python3

#
# This command requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.lib.storage import LocalStorage
from hatsploit.lib.command import Command
from hatsploit.lib.modules import Modules


class HatSploitCommand(Command):
    modules = Modules()
    local_storage = LocalStorage()

    details = {
        'Category': "module",
        'Name': "back",
        'Authors': [
            'Ivan Nikolsky (enty8080)'
        ],
        'Description': "Return to the previous module.",
        'Usage': "back",
        'MinArgs': 0
    }

    def run(self, argc, argv):
        if self.modules.check_current_module():
            self.local_storage.set("current_module_number", self.local_storage.get("current_module_number") - 1)
            self.local_storage.set("current_module", self.local_storage.get("current_module")[0:-1])
            if not self.local_storage.get("current_module"):
                self.local_storage.set("current_module_number", 0)
