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
            'Name': "unset",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - command developer',
            ],
            'Description': "Unset an option / Set to None.",
            'Usage': "unset <option>",
            'MinArgs': 1,
        })

        self.modules = Modules()

    def run(self, args):
        self.modules.set_current_module_option(args[1])
