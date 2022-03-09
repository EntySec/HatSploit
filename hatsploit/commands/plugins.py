#!/usr/bin/env python3

#
# This command requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.lib.command import Command
from hatsploit.lib.show import Show


class HatSploitCommand(Command):
    show = Show()

    details = {
        'Category': "plugins",
        'Name': "plugins",
        'Authors': [
            'Ivan Nikolsky (enty8080) - command developer'
        ],
        'Description': "Show available plugins.",
        'Usage': "plugins",
        'MinArgs': 0
    }

    def run(self, argc, argv):
        self.show_plugins()
