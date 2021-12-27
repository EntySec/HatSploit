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

    usage = ""
    usage += "loot <option> [arguments]\n\n"
    usage += "  -l, --list           List all collected loot.\n"
    usage += "  -r, --remove <name>  Remove collected loot.\n"

    details = {
        'Category': "loot",
        'Name': "loot",
        'Authors': [
            'Ivan Nikolsky (enty8080) - command developer'
        ],
        'Description': "Manage collected loot.",
        'Usage': usage,
        'MinArgs': 1
    }

    def run(self, argc, argv):
        choice = argv[1]
        if choice in ['-l', '--list']:
            self.show.show_loot()

        elif choice in ['-r', '--remove']:
            if argc < 3:
                self.print_usage(self.details['Usage'])
            else:
                self.loot.remove_loot(argv[2])
        else:
            self.print_usage(self.details['Usage'])
