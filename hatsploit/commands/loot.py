#!/usr/bin/env python3

#
# This command requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.lib.command import Command
from hatsploit.lib.loot import Loot
from hatsploit.lib.show import Show


class HatSploitCommand(Command):
    loot = Loot()
    show = Show()

    details = {
        'Category': "loot",
        'Name': "loot",
        'Authors': [
            'Ivan Nikolsky (enty8080) - command developer'
        ],
        'Description': "Manage collected loot.",
        'Usage': "loot <option> [arguments]",
        'MinArgs': 1,
        'Options': {
            '-l': ['', "List all collected loot."],
            '-r': ['<name>', "Remove collected loot."]
        }
    }

    def run(self, argc, argv):
        choice = argv[1]

        if choice == '-l':
            self.show.show_loot()

        elif choice == '-r':
            self.loot.remove_loot(argv[2])
