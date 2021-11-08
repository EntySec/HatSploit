#!/usr/bin/env python3

#
# This command requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

import os

from hatsploit.lib.command import Command
from hatsploit.lib.log import Log


class HatSploitCommand(Command):
    log = Log()

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
        option = argv[1]
        if option == "on":
            if argc < 3:
                self.print_usage(self.details['Usage'])
            else:
                self.log.enable_log(argv[1])
        elif option == "off":
            self.log.disable_log()
        else:
            self.print_usage(self.details['Usage'])
