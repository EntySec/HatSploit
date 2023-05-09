"""
This command requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.core.utils.ui.tip import Tip
from hatsploit.lib.command import Command


class HatSploitCommand(Command):
    def __init__(self):
        super().__init__()

        self.tip = Tip()

        self.details = {
            'Category': "misc",
            'Name': "tip",
            'Authors': [
                'Ivan Nikolsky (enty8080) - command developer',
            ],
            'Description': "Show random HatSploit tip.",
            'Usage': "tip",
            'MinArgs': 0,
        }

    def run(self, argc, argv):
        self.tip.print_random_tip()
