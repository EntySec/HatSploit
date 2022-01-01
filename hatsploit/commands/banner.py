#!/usr/bin/env python3

#
# This command requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.lib.command import Command

from hatsploit.core.utils.ui.banner import Banner


class HatSploitCommand(Command):
    banner = Banner()

    details = {
        'Category': "misc",
        'Name': "banner",
        'Authors': [
            'Ivan Nikolsky (enty8080) - command developer'
        ],
        'Description': "Show random HatSploit banner.",
        'Usage': "banner",
        'MinArgs': 0
    }

    def run(self, argc, argv):
        self.banner.print_random_banner()
