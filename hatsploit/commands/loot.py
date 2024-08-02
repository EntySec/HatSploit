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
            'Category': "loot",
            'Name': "loot",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - command developer',
            ],
            'Description': "Manage collected loot.",
            'Usage': "loot <option> [arguments]",
            'MinArgs': 1,
            'Options': {
                'list': ['', "List all collected loot."],
                'remove': ['<name>', "Remove collected loot."],
            },
        })

        self.loot = Loot()
        self.show = Show()

    def run(self, args):
        if args[1] == 'list':
            self.show.show_loot(self.loot.list_loot())

        elif args[1] == 'remove':
            self.loot.remove_loot(args[2])
