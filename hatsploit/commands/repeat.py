#!/usr/bin/env python3

#
# This command requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.core.base.execute import Execute
from hatsploit.lib.command import Command


class HatSploitCommand(Command):
    execute = Execute()

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
        times = argv[0]
        command = argv[1]

        if times.isdigit():
            commands = command.split()
            arguments = ""
            if commands:
                arguments = command.replace(commands[0], "", 1).strip()

            for _ in range(int(times)):
                self.execute.execute_command(commands, arguments)
        else:
            self.output_error("Times expected!")
