"""
This command requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

import time

from hatsploit.core.base.execute import Execute
from hatsploit.lib.command import Command


class HatSploitCommand(Command):
    def __init__(self):
        super().__init__()

        self.execute = Execute()

        self.details.update({
            'Category': "developer",
            'Name': "sleep",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - command developer',
            ],
            'Description': "Sleep for specified seconds.",
            'Usage': "sleep <seconds>",
            'MinArgs': 1,
        })

    def run(self, argc, argv):
        try:
            time.sleep(float(argv[1]))
        except ValueError:
            self.print_error("Seconds expected!")
