#!/usr/bin/env python3

#
# This command requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.lib.command import Command
from hatsploit.lib.commands import Commands


class HatSploitCommand(Command):
    commands = Commands()

    details = {
        'Category': "core",
        'Name': "help",
        'Authors': [
            'Ivan Nikolsky (enty8080) - command developer'
        ],
        'Description': "Show available commands.",
        'Usage': "help",
        'MinArgs': 0
    }

    def run(self, argc, argv):
        self.commands.execute_command(['?'])
