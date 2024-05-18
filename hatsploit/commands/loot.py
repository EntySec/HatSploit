"""
This command requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.command import Command
from hatsploit.lib.loot import Loot
from hatsploit.lib.show import Show


class HatSploitCommand(Command):
    def __init__(self):
        super().__init__()

        self.loot = Loot()
        self.show = Show()

        self.details.update({
            'Category': "loot",
            'Name': "loot",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - command developer',
            ],
            'Description': "Manage collected loot.",
            'Usage': "loot <option> [arguments]",
            'MinArgs': 1,
            'Options': {
                '-l': ['', "List all collected loot."],
                '-r': ['<name>', "Remove collected loot."],
            },
        })

    def run(self, argc, argv):
        choice = argv[1]

        if choice == '-l':
            self.show.show_loot(self.loot.list_loot())

        elif choice == '-r':
            self.loot.remove_loot(argv[2])
