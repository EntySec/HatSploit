"""
This command requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.command import Command
from hatsploit.lib.modules import Modules
from hatsploit.lib.show import Show


class HatSploitCommand(Command):
    def __init__(self):
        super().__init__()

        self.modules = Modules()
        self.show = Show()

        self.details.update({
            'Category': "modules",
            'Name': "devices",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - command developer',
            ],
            'Description': "Display devices supported by module.",
            'Usage': "devices",
            'MinArgs': 0,
        })

    def run(self, argc, argv):
        self.show.show_module_devices(
            self.modules.get_current_module())
