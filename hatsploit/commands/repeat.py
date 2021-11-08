#!/usr/bin/env python3

#
# This command requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.lib.commands import Commands
from hatsploit.lib.command import Command


class HatSploitCommand(Command):
    commands = Commands()

    details = {
        'Category': "developer",
        'Name': "repeat",
        'Authors': [
            'Ivan Nikolsky (enty8080) - command developer'
        ],
        'Description': "Repeat specified command.",
        'Usage': "repeat <times> <command>",
        'MinArgs': 2
    }

    def run(self, argc, argv):
        if times.isdigit():
            commands = self.format_commands(argv[2])

            for _ in range(int(argv[1])):
                self.commands.execute_command(commands)
        else:
            self.print_error("Times expected!")
