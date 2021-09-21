#!/usr/bin/env python3

#
# This command requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.lib.config import Config
from hatsploit.lib.storage import GlobalStorage
from hatsploit.lib.command import Command


class HatSploitCommand(Command):
    config = Config()

    storage_path = config.path_config['storage_path']
    global_storage = GlobalStorage(storage_path)

    usage = ""
    usage += "log <option>\n\n"
    usage += "  on <file>/off  Turn logging on/off.\n"

    details = {
        'Category': "developer",
        'Name': "log",
        'Authors': [
            'Ivan Nikolsky (enty8080) - command developer'
        ],
        'Description': "Log HatSploit output to log file.",
        'Usage': usage,
        'MinArgs': 1
    }

    def run(self, argc, argv):
        option = argv[0]
        if option == "on":
            if argc < 2:
                self.print_usage(self.details['Usage'])
            else:
                if os.access(argv[1], os.R_OK):
                    self.global_storage.set("log", argv[1])
                    self.global_storage.set_all()
                    self.print_information("HatSploit log: on")
        elif option == "off":
            self.global_storage.set("log", None)
            self.global_storage.set_all()
            self.print_information("HatSploit log: off")
        else:
            self.print_usage(self.details['Usage'])
