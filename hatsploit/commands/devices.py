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
            'Name': "devices",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - command developer',
            ],
            'Description': "Display devices supported by module.",
            'Usage': "devices",
            'MinArgs': 0,
        })

        self.modules = Modules()

    def run(self, _):
        Show().show_module_devices(
            self.modules.get_current_module())
