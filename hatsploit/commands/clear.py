#!/usr/bin/env python3

#
# This command requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.lib.command import Command


class HatSploitCommand(Command):
    details = {
        'Category': "core",
        'Name': "clear",
        'Authors': [
            'Ivan Nikolsky (enty8080) - command developer'
        ],
        'Description': "Clear terminal window.",
        'Usage': "clear",
        'MinArgs': 0
    }

    def run(self, argc, argv):
        self.print_empty(self.CLEAR, end='')
