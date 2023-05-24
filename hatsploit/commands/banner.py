"""
This command requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.core.utils.ui.banner import Banner
from hatsploit.lib.command import Command


class HatSploitCommand(Command):
    def __init__(self):
        super().__init__()

        self.banner = Banner()

        self.details.update({
            'Category': "misc",
            'Name': "banner",
            'Authors': [
                'Ivan Nikolsky (enty8080) - command developer',
            ],
            'Description': "Show random HatSploit banner.",
            'Usage': "banner",
            'MinArgs': 0,
        })

    def run(self, argc, argv):
        self.banner.print_random_banner()
