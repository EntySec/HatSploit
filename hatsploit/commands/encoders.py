"""
This command requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from badges.cmd import Command
from hatsploit.lib.ui.encoders import Encoders
from hatsploit.lib.ui.show import Show


class ExternalCommand(Command):
    def __init__(self):
        super().__init__({
            'Category': "encoder",
            'Name': "encoders",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - command developer',
            ],
            'Description': "Show available encoders.",
        })

        self.encoders = Encoders()

    def rpc(self, *_):
        return self.encoders.get_encoders()

    def run(self, _):
        Show().show_encoders(self.encoders.get_encoders())
