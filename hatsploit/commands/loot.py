"""
This command requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from badges.cmd import Command
from hatsploit.lib.loot import Loot
from hatsploit.lib.ui.show import Show


class ExternalCommand(Command):
    def __init__(self):
        super().__init__({
            'Category': "manage",
            'Name': "loot",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - command developer',
            ],
            'Description': "Manage collected loot.",
            'MinArgs': 1,
            'Options': [
                (
                    ('-l', '--list'),
                    {
                        'help': "List all collected loot.",
                        'action': 'store_true'
                    }
                ),
                (
                    ('-r', '--remove'),
                    {
                        'help': 'Remove collected loot by name.',
                        'metavar': 'NAME'
                    }
                )
            ]
        })

        self.loot = Loot()
        self.show = Show()

    def run(self, args):
        if args.list:
            self.show.show_loot(self.loot.list_loot())

        elif args.remove:
            self.loot.remove_loot(args[2])
