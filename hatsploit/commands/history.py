#!/usr/bin/env python3

#
# This command requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.lib.command import Command
from hatsploit.lib.history import History


class HatSploitCommand(Command):
    history = History()

    details = {
        'Category': "developer",
        'Name': "history",
        'Authors': [
            'Ivan Nikolsky (enty8080) - command developer'
        ],
        'Description': "Manage HatSploit history.",
        'MinArgs': 1,
        'Options': {
            '-l': 'List all history.',
            '-c': 'Clear all history.',
            'on': 'Turn history on.',
            'off': 'Turn history off.'
        }
    }

    def run(self, argc, argv):
        option = argv[1]
        if option == "on":
            self.history.enable_history()

        elif option == "off":
            self.history.disable_history()

        elif option == '-c':
            self.history.clear_history()

        elif option == '-l':
            self.history.list_history()
        else:
            self.print_usage(self.details['Usage'])
