"""
This command requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from badges.cmd import Command

from hatsploit.lib.ui.modules import Modules
from hatsploit.lib.ui.show import Show


class ExternalCommand(Command):
    def __init__(self):
        super().__init__({
            'Category': "modules",
            'Name': "advanced",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - command developer',
            ],
            'Description': "Show current module advanced options.",
            'Usage': "options",
            'MinArgs': 0,
        })

        self.modules = Modules()

    def rpc(self, *_):
        return self.modules.get_current_advanced()

    def run(self, _):
        Show().show_advanced(self.modules.get_current_module())
