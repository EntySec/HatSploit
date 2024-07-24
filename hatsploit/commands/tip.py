"""
This command requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.core.utils.ui.tip import Tip
from badges.cmd import Command


class ExternalCommand(Command):
    def __init__(self):
        super().__init__({
            'Category': "misc",
            'Name': "tip",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - command developer',
            ],
            'Description': "Show random HatSploit tip.",
            'Usage': "tip",
            'MinArgs': 0,
        })

    def run(self, _):
        Tip().print_random_tip()
