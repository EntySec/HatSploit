"""
This command requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.command import Command
from hatsploit.lib.history import History


class HatSploitCommand(Command):
    def __init__(self):
        super().__init__()

        self.history = History()

        self.details = {
            'Category': "developer",
            'Name': "history",
            'Authors': [
                'Ivan Nikolsky (enty8080) - command developer',
            ],
            'Description': "Manage HatSploit history.",
            'Usage': "history <option>",
            'MinArgs': 1,
            'Options': {
                '-l': ['', "List all history."],
                '-c': ['', "Clear all history."],
                'on': ['', "Turn history on."],
                'off': ['', "Turn history off."],
            },
        }

    def run(self, argc, argv):
        option = argv[1]

        if option == 'on':
            self.history.enable_history()

        elif option == 'off':
            self.history.disable_history()

        elif option == '-c':
            self.history.clear_history()

        elif option == '-l':
            for entry in self.history.list_history():
                self.print_empty(entry)
