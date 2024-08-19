"""
This command requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from badges.cmd import Command
from hatsploit.lib.ui.history import History


class ExternalCommand(Command):
    def __init__(self):
        super().__init__({
            'Category': "manage",
            'Name': "history",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - command developer',
            ],
            'Description': "Manage HatSploit command history.",
            'MinArgs': 1,
            'Options': [
                (
                    ('-l', '--list'),
                    {
                        'help': "List collected command history.",
                        'action': 'store_true'
                    }
                ),
                (
                    ('-c', '--clear'),
                    {
                        'help': "Clear collected command history",
                        'action': 'store_true'
                    }
                ),
                (
                    ('-d', '--disable'),
                    {
                        'help': "Disable command history.",
                        'action': 'store_true'
                    }
                ),
                (
                    ('-e', '--enable'),
                    {
                        'help': "Enable command history.",
                        'action': 'store_true'
                    }
                )
            ]
        })

        self.history = History()

    def run(self, args):
        if args.enable:
            self.history.enable_history()

        elif args.disable:
            self.history.disable_history()

        elif args.clear:
            self.history.clear_history()

        elif args.list:
            for entry in self.history.list_history():
                self.print_empty(entry)
