"""
This command requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.command import Command
from hatsploit.lib.payloads import Payloads
from hatsploit.lib.show import Show


class HatSploitCommand(Command):
    payloads = Payloads()
    show = Show()

    details = {
        'Category': "modules",
        'Name': "payloads",
        'Authors': [
            'Ivan Nikolsky (enty8080) - command developer',
        ],
        'Description': "Show available payloads.",
        'Usage': "payloads",
        'MinArgs': 0,
    }

    def run(self, argc, argv):
        self.show.show_payloads()
