#!/usr/bin/env python3

#
# This command requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

import readline

from hatsploit.lib.command import Command
from hatsploit.lib.config import Config
from hatsploit.lib.storage import GlobalStorage
from hatsploit.lib.storage import LocalStorage


class HatSploitCommand(Command):
    config = Config()
    local_storage = LocalStorage()

    history = config.path_config['history_path']
    storage_path = config.path_config['storage_path']

    global_storage = GlobalStorage(storage_path)

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

    def run(self, argc, argv):
        option = argv[1]
        if option == "on":
            self.global_storage.set("history", True)
            self.global_storage.set_all()
            self.print_information("HatSploit history: on")

        elif option == "off":
            self.global_storage.set("history", False)
            self.global_storage.set_all()
            readline.clear_history()
            with open(self.history, 'w') as history:
                history.write("")
            self.print_information("HatSploit history: off")

        elif option in ['-c', '--clear']:
            readline.clear_history()
            with open(self.history, 'w') as history:
                history.write("")

        elif option in ['-l', '--list']:
            using_history = self.local_storage.get("history")
            if using_history:
                if readline.get_current_history_length() > -1:
                    self.print_information("HatSploit history:")

                    for index in range(1, readline.get_current_history_length() + 1):
                        self.print_empty("    * " + readline.get_history_item(index))
                else:
                    self.print_warning("HatSploit history empty.")
            else:
                self.print_warning("No HatSploit history detected.")
        else:
            self.print_usage(self.details['Usage'])
