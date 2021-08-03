#!/usr/bin/env python3

#
# This command requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

import time

from hatsploit.core.base.execute import Execute
from hatsploit.lib.command import Command


class HatSploitCommand(Command):
    execute = Execute()

    details = {
        'Category': "developer",
        'Name': "sleep",
        'Authors': [
            'Ivan Nikolsky (enty8080) - command developer'
        ],
        'Description': "Sleep for specified seconds.",
        'Usage': "sleep <seconds>",
        'MinArgs': 1
    }

    def run(self, argc, argv):
        seconds = argv[0]

        if seconds.replace('.', '', 1).isdigit():
            time.sleep(float(seconds))
        else:
            self.print_error("Seconds expected!")
