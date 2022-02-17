#!/usr/bin/env python3

#
# This command requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.lib.command import Command
from hatsploit.lib.history import History


class HatSploitCommand(Command):
    history = History()

    usage = ""
    usage += "history <option>\n\n"
    usage += "  -l, --list   List all history.\n"
    usage += "  -c, --clear  Clear all history.\n"
    usage += "  on/off       Turn history on/off.\n"

    details = {
        'Category': "developer",
        'Name': "history",
        'Authors': [
            'Ivan Nikolsky (enty8080) - command developer'
        ],
        'Description': "Manage HatSploit history.",
        'Usage': usage,
        'MinArgs': 1
    }

    def complete(self, text):
        options = ['-l', '-c', '--list',
                   '--clear', 'on', 'off']
        return [option for option in options if option.startswith(text)]

    def run(self, argc, argv):
        option = argv[1]
        if option == "on":
            self.history.enable_history()

        elif option == "off":
            self.history.disable_history()

        elif option in ['-c', '--clear']:
            self.history.clear_history()

        elif option in ['-l', '--list']:
            self.history.list_history()
        else:
            self.print_usage(self.details['Usage'])
