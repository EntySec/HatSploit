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
            'Name': "set",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - command developer',
            ],
            'Description': "Set an option value.",
            'Usage': "set <option> <value>",
            'MinArgs': 2,
        })

    def rpc(self, *args):
        if len(args) < 2:
            return

        self.modules.set_current_module_option(args[0].lower(), args[1])

    def run(self, argc, argv):
        self.modules.set_current_module_option(argv[1].lower(), argv[2])
