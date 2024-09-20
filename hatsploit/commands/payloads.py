"""
This command requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from badges.cmd import Command
from hatsploit.lib.ui.payloads import Payloads
from hatsploit.lib.ui.show import Show


class ExternalCommand(Command):
    def __init__(self):
        super().__init__({
            'Category': "modules",
            'Name': "payloads",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - command developer',
            ],
            'Description': "Show available payloads.",
        })

        self.payloads = Payloads()
        self.show = Show()

    def rpc(self, *_):
        return self.payloads.get_payloads()

    def run(self, _):
        self.show.show_payloads(self.payloads.get_payloads())
