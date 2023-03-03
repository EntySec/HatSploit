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
            'Name': "use",
            'Authors': [
                'Ivan Nikolsky (enty8080) - command developer',
            ],
            'Description': "Use specified module.",
            'Usage': "use <module|number>",
            'MinArgs': 1,
        }

    complete = modules.modules_completer

    def run(self, argc, argv):
        self.modules.use_module(argv[1])
