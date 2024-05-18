"""
This command requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.command import Command
from hatsploit.lib.encoders import Encoders
from hatsploit.lib.show import Show


class HatSploitCommand(Command):
    def __init__(self):
        super().__init__()

        self.show = Show()
        self.encoders = Encoders()

        self.details.update({
            'Category': "encoder",
            'Name': "encoders",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - command developer',
            ],
            'Description': "Show available encoders.",
            'Usage': "encoders",
            'MinArgs': 0,
        })

    def rpc(self, *args):
        return self.encoders.get_encoders()

    def run(self, argc, argv):
        self.show.show_encoders(self.encoders.get_encoders())
