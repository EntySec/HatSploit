#!/usr/bin/env python3

#
# This command requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.lib.storage import LocalStorage
from hatsploit.lib.command import Command


class HatSploitCommand(Command):
    local_storage = LocalStorage()

    usage = ""
    usage += "spool <option>\n\n"
    usage += "  on <file>/off  Turn spooling on/off.\n"

    details = {
        'Category': "developer",
        'Name': "spool",
        'Authors': [
            'Ivan Nikolsky (enty8080) - command developer'
        ],
        'Description': "Log HatSploit output to spool file.",
        'Usage': usage,
        'MinArgs': 1
    }

    def run(self, argc, argv):
        option = argv[0]
        if option == "on":
            if argc < 2:
                self.output_usage(self.details['Usage'])
            else:
                self.local_storage.set("spool", argv[1])
                self.output_information("HatSploit spool: on")
        elif option == "off":
            self.local_storage.set("spool", None)
            self.output_information("HatSploit spool: off")
        else:
            self.output_usage(self.details['Usage'])
