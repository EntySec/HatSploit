"""
This command requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.command import Command
from hatsploit.lib.show import Show

from hatsploit.lib.modules import Modules
from hatsploit.lib.payloads import Payloads
from hatsploit.lib.encoders import Encoders
from hatsploit.lib.plugins import Plugins


class HatSploitCommand(Command):
    def __init__(self):
        super().__init__()

        self.show = Show()
        self.modules = Modules()
        self.payloads = Payloads()
        self.encoders = Encoders()
        self.plugins = Plugins()

        self.details.update({
            'Category': "core",
            'Name': "search",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - command developer',
            ],
            'Description': "Search payloads, modules and plugins.",
            'Usage': "search [where] <keyword>",
            'MinArgs': 1,
        })

    def run(self, argc, argv):
        if argc > 2:
            if argv[1] == 'modules':
                self.show.show_search_modules(
                    self.modules.get_modules(), argv[2])

            elif argv[1] == 'payloads':
                self.show.show_search_payloads(
                    self.payloads.get_payloads(), argv[2])

            elif argv[1] == 'encoders':
                self.show.show_search_encoders(
                    self.encoders.get_encoders(), argv[2])

            elif argv[1] == 'plugins':
                self.show.show_search_plugins(
                    self.plugins.get_plugins(), argv[2])
            return

        self.show.show_search_modules(
            self.modules.get_modules(), argv[1])
        self.show.show_search_payloads(
            self.payloads.get_payloads(), argv[1])
        self.show.show_search_encoders(
            self.encoders.get_encoders(), argv[1])
        self.show.show_search_plugins(
            self.plugins.get_plugins(), argv[1])
