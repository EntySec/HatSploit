#!/usr/bin/env python3

#
# This command requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.lib.command import Command

from hatsploit.core.utils.ui.tip import Tip


class HatSploitCommand(Command):
    tip = Tip()

    details = {
        'Category': "misc",
        'Name': "tip",
        'Authors': [
            'Ivan Nikolsky (enty8080) - command developer'
        ],
        'Description': "Show random HatSploit tip.",
        'Usage': "tip",
        'MinArgs': 0
    }

    def run(self, argc, argv):
        self.tip.print_random_tip()
