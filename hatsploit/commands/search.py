#!/usr/bin/env python3

#
# This command requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.lib.command import Command
from hatsploit.lib.show import Show


class HatSploitCommand(Command):
    show = Show()

    usage = ""
    usage += "search [option] [<keyword>]\n\n"
    usage += "  -w, --where [payloads|modules|plugins]  Select where to search.\n"

    details = {
        'Category': "core",
        'Name': "search",
        'Authors': [
            'Ivan Nikolsky (enty8080) - command developer'
        ],
        'Description': "Search payloads, modules and plugins.",
        'Usage': "search [option] [<keyword>]",
        'MinArgs': 1,
        'Options': {
            '-w': ['[payloads|modules|plugins]', "Select where to search."]
        }
    }

    def run(self, argc, argv):
        if argv[1] not in ['-w', '--where']:
            self.show.show_search_modules(argv[1])
            self.show.show_search_payloads(argv[1])
            self.show.show_search_plugins(argv[1])
        else:
            if argv[2] == 'modules':
                self.show.show_search_modules(argv[3])
            elif argv[2] == 'payloads':
                self.show.show_search_payloads(argv[3])
            elif argv[2] == 'plugins':
                self.show.show_search_plugins(argv[3])
