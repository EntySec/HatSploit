"""
This command requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

import time

from badges.cmd import Command


class ExternalCommand(Command):
    def __init__(self):
        super().__init__({
            'Category': "developer",
            'Name': "sleep",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - command developer',
            ],
            'Description': "Sleep for specified seconds.",
            'Usage': "sleep <seconds>",
            'MinArgs': 1,
        })

    def run(self, args):
        try:
            time.sleep(float(args[1]))
        except ValueError:
            self.print_error("Seconds expected!")
