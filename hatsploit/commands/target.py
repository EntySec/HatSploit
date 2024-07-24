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
            'Name': "target",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - command developer',
            ],
            'Description': "Set module target if available.",
            'Usage': "target <id>",
            'MinArgs': 1,
        })

        self.modules = Modules()

    def rpc(self, *args):
        if len(args) < 1:
            return

        self.modules.set_current_module_target(int(args[0]))

    def run(self, args):
        if not self.modules.set_current_module_target(int(args[1])):
            self.print_error(f"Invalid target ID: {args[1]}!")
