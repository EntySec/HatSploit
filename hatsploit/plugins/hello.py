"""
This plugin requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from badges.cmd import Command
from hatsploit.lib.core.plugin import Plugin


class HatSploitPlugin(Plugin):
    def __init__(self):
        super().__init__({
            'Name': "Hello World",
            'Plugin': "hello",
            'Authors': [
                'Your name (your nickname) - plugin developer',
            ],
            'Description': "",
        })

        self.commands = {
            Command({
                'Name': 'hello',
                'Description': "Hello.",
                'MinArgs': 1, # Minimum number of arguments
                'Options': [
                    (  # command options (argparse)
                        ('-o', '--oppa'),
                        {
                            'help': "Oppa.",
                        }
                    ),
                    # other command options
                ]
            })
        }

    # command body, name of method should be a name of command
    def hello(self, args):
        self.print_empty(args.oppa)

    # method executed during the loading process
    def load(self):
        self.print_empty('Hello there!')

    # method executed during the unloading process
    def unload(self):
        self.print_empty('Bye :(')
