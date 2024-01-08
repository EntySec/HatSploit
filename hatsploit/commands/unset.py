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
            'Name': "unset",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - command developer',
            ],
            'Description': "Unset an option / Set to None.",
            'Usage': "unset <option>",
            'MinArgs': 1,
        })

    def run(self, argc, argv):
        self.modules.set_current_module_option(argv[1].lower())
