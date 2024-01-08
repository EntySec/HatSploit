"""
This command requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.command import Command
from hatsploit.lib.show import Show


class HatSploitCommand(Command):
    def __init__(self):
        super().__init__()

        self.show = Show()

        self.details.update({
            'Category': "core",
            'Name': "search",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - command developer',
            ],
            'Description': "Search payloads, modules and plugins.",
            'Usage': "search <option> <keyword>",
            'MinArgs': 2,
            'Options': {
                '-w': ['[payloads|encoders|modules|plugins]', "Select where to search."],
                '-e': ['', "Search everywhere."],
            },
        })

    def run(self, argc, argv):
        if argv[1] not in ['-w', '--where']:
            self.show.show_search_modules(argv[2])
            self.show.show_search_payloads(argv[2])
            self.show.show_search_encoders(argv[2])
            self.show.show_search_plugins(argv[2])
        else:
            if argv[2] == 'modules':
                self.show.show_search_modules(argv[3])
            elif argv[2] == 'payloads':
                self.show.show_search_payloads(argv[3])
            elif argv[2] == 'encoders':
                self.show.show_search_encoders(argv[3])
            elif argv[2] == 'plugins':
                self.show.show_search_plugins(argv[3])
