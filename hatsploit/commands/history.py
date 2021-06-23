#!/usr/bin/env python3

#
# This command requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

import readline

from hatsploit.core.base.config import Config
from hatsploit.core.base.storage import GlobalStorage
from hatsploit.core.base.storage import LocalStorage
from hatsploit.command import Command


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
            'Ivan Nikolsky (enty8080)'
        ],
        'Description': "Manage HatSploit history.",
        'Usage': usage,
        'MinArgs': 1
    }

    def run(self, argc, argv):
        option = argv[0]
        if option == "on":
            self.local_storage.set("history", True)
            self.global_storage.set("history", True)
            self.output_information("HatSploit history: on")
        elif option == "off":
            self.local_storage.set("history", False)
            self.global_storage.set("history", False)
            self.output_information("HatSploit history: off")
        elif option in ['-c', '--clear']:
            readline.clear_history()
            with open(self.history, 'w') as history:
                history.write("")
        elif option in ['-l', '--list']:
            using_history = self.local_storage.get("history")
            if using_history:
                if readline.get_current_history_length() > 0:
                    self.output_information("HatSploit history:")

                    history_file = open(self.history, 'r')
                    history = [x.strip() for x in history_file.readlines()]
                    history_file.close()
                    for line in history:
                        self.output_empty("    * " + line)

                    for index in range(1, readline.get_current_history_length()):
                        self.output_empty("    * " + readline.get_history_item(index))
                else:
                    self.output_warning("HatSploit history empty.")
            else:
                self.output_warning("No history detected.")
        else:
            self.output_usage(self.details['Usage'])
