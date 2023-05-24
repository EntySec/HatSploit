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

        self.details.update({
            'Category': "modules",
            'Name': "use",
            'Authors': [
                'Ivan Nikolsky (enty8080) - command developer',
            ],
            'Description': "Use specified module.",
            'Usage': "use <module|number>",
            'MinArgs': 1,
        })

        self.complete = self.modules.modules_completer

    def rpc(self, *args):
        if len(args) < 1:
            return

        self.modules.use_module(args[0])

    def run(self, argc, argv):
        self.modules.use_module(argv[1])
