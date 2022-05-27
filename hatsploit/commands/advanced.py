#!/usr/bin/env python3

#
# This command requires HatSploit: https://hatsploit.com
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.lib.command import Command
from hatsploit.lib.show import Show


class HatSploitCommand(Command):
    show = Show()

    details = {
        'Category': "modules",
        'Name': "advanced",
        'Authors': ['Ivan Nikolsky (enty8080) - command developer'],
        'Description': "Show current module advanced options.",
        'Usage': "options",
        'MinArgs': 0,
    }

    def run(self, argc, argv):
        self.show.show_advanced()
