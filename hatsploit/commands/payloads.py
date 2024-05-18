"""
This command requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.command import Command
from hatsploit.lib.payloads import Payloads
from hatsploit.lib.show import Show


class HatSploitCommand(Command):
    def __init__(self):
        super().__init__()

        self.payloads = Payloads()
        self.show = Show()

        self.details.update({
            'Category': "modules",
            'Name': "payloads",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - command developer',
            ],
            'Description': "Show available payloads.",
            'Usage': "payloads",
            'MinArgs': 0,
        })

    def rpc(self, *args):
        return self.payloads.get_payloads()

    def run(self, argc, argv):
        self.show.show_payloads(self.payloads.get_payloads())
