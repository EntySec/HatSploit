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

        self.show = Show()
        self.modules = Modules()

        self.details.update({
            'Category': "modules",
            'Name': "advanced",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - command developer',
            ],
            'Description': "Show current module advanced options.",
            'Usage': "options",
            'MinArgs': 0,
        })

    def rpc(self, *args):
        return self.modules.get_current_advanced()

    def run(self, argc, argv):
        self.show.show_advanced(self.modules.get_current_module())
