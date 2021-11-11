#!/usr/bin/env python3

#
# This command requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.lib.command import Command


class HatSploitCommand(Command):
    details = {
        'Category': "gather",
        'Name': "sysinfo",
        'Authors': [
            'Ivan Nikolsky (enty8080) - command developer'
        ],
        'Description': "Show device system information.",
        'Usage': "sysinfo",
        'MinArgs': 0
    }

    def run(self, argc, argv):
        output = self.session.send_command(
            ' '.join(argv), True
        )

        if output:
            self.print_empty(output)
