"""
This command requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.command import Command
from hatsploit.lib.modules import Modules


class HatSploitCommand(Command):
    def __init__(self):
        super().__init__()

        self.modules = Modules()

        self.details = {
            'Category': "modules",
            'Name': "back",
            'Authors': [
                'Ivan Nikolsky (enty8080) - command developer',
            ],
            'Description': "Return to the previous module.",
            'Usage': "back",
            'MinArgs': 0,
        }

    def rpc(self, *args):
        self.run(0, [])

    def run(self, argc, argv):
        self.modules.go_back()
