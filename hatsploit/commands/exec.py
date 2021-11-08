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
        'Category': "developer",
        'Name': "exec",
        'Authors': [
            'Ivan Nikolsky (enty8080) - command developer'
        ],
        'Description': "Execute local system command.",
        'Usage': "exec <command>",
        'MinArgs': 1
    }

    def run(self, argc, argv):
        commands = self.format_commands(argv[1])
        self.commands.execute_system_command(commands)
