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
        'Name': "back",
        'Authors': [
            'Ivan Nikolsky (enty8080) - command developer'
        ],
        'Description': "Return to the previous module.",
        'Usage': "back",
        'MinArgs': 0
    }

    def run(self, argc, argv):
        self.modules.go_back()
