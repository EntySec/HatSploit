"""
This command requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.command import Command
from hatsploit.lib.plugins import Plugins


class HatSploitCommand(Command):
    def __init__(self):
        super().__init__()

        self.plugins = Plugins()

        self.details = {
            'Category': "plugins",
            'Name': "load",
            'Authors': [
                'Ivan Nikolsky (enty8080) - command developer',
            ],
            'Description': "Load specific plugin.",
            'Usage': "load <plugin|number>",
            'MinArgs': 1,
        }

        self.complete = self.plugins.plugins_completer

    def run(self, argc, argv):
        self.plugins.load_plugin(argv[1])
