"""
This command requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from badges.cmd import Command
from hatsploit.lib.ui.show import Show

from hatsploit.lib.ui.modules import Modules
from hatsploit.lib.ui.payloads import Payloads
from hatsploit.lib.ui.encoders import Encoders
from hatsploit.lib.ui.plugins import Plugins


class ExternalCommand(Command):
    def __init__(self):
        super().__init__({
            'Category': "core",
            'Name': "search",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - command developer',
            ],
            'Description': "Search payloads, modules and plugins.",
            'Usage': "search [where] <keyword>",
            'MinArgs': 1,
        })

        self.show = Show()
        self.modules = Modules()
        self.payloads = Payloads()
        self.encoders = Encoders()
        self.plugins = Plugins()

    def run(self, args):
        if len(args) > 2:
            if args[1] == 'modules':
                self.show.show_search_modules(
                    self.modules.get_modules(), args[2])

            elif args[1] == 'payloads':
                self.show.show_search_payloads(
                    self.payloads.get_payloads(), args[2])

            elif args[1] == 'encoders':
                self.show.show_search_encoders(
                    self.encoders.get_encoders(), args[2])

            elif args[1] == 'plugins':
                self.show.show_search_plugins(
                    self.plugins.get_plugins(), args[2])
            return

        self.show.show_search_modules(
            self.modules.get_modules(), args[1])
        self.show.show_search_payloads(
            self.payloads.get_payloads(), args[1])
        self.show.show_search_encoders(
            self.encoders.get_encoders(), args[1])
        self.show.show_search_plugins(
            self.plugins.get_plugins(), args[1])
