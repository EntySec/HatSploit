"""
This command requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from badges.cmd import Command
from hatsploit.lib.ui.history import History


class ExternalCommand(Command):
    def __init__(self):
        super().__init__({
            'Category': "developer",
            'Name': "history",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - command developer',
            ],
            'Description': "Manage HatSploit history.",
            'Usage': "history <option>",
            'MinArgs': 1,
            'Options': {
                'list': ['', "List all history."],
                'clear': ['', "Clear all history."],
                'on': ['', "Turn history on."],
                'off': ['', "Turn history off."],
            },
        })

        self.history = History()

    def run(self, args):
        if args[1] == 'on':
            self.history.enable_history()

        elif args[1] == 'off':
            self.history.disable_history()

        elif args[1] == 'clear':
            self.history.clear_history()

        elif args[1] == 'list':
            for entry in self.history.list_history():
                self.print_empty(entry)
