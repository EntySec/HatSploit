"""
This command requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.command import Command
from hatsploit.lib.modules import Modules


class HatSploitCommand(Command):
    def __init__(self):
        super().__init__()

        self.modules = Modules()

        self.details.update({
            'Category': "modules",
            'Name': "target",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - command developer',
            ],
            'Description': "Set module target if available.",
            'Usage': "target <id>",
            'MinArgs': 1,
        })

    def rpc(self, *args):
        if len(args) < 1:
            return

        self.modules.set_current_module_target(int(args[0]))

    def run(self, argc, argv):
        if not self.modules.set_current_module_target(int(argv[1])):
            self.print_error(f"Invalid target ID: {argv[1]}!")
