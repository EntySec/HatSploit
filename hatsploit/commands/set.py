"""
This command requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from badges.cmd import Command
from hatsploit.lib.ui.modules import Modules


class ExternalCommand(Command):
    def __init__(self):
        super().__init__({
            'Category': "modules",
            'Name': "set",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - command developer',
            ],
            'Description': "Set an option value.",
            'Usage': "set <option> <value>",
            'MinArgs': 2,
        })

        self.modules = Modules()

    def rpc(self, *args):
        if len(args) < 2:
            return

        self.modules.set_current_module_option(args[0], args[1])

    def run(self, args):
        self.modules.set_current_module_option(args[1], args[2])
