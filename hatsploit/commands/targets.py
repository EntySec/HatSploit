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
            'Name': "targets",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - command developer',
            ],
            'Description': "Display available module targets.",
            'Usage': "targets",
            'MinArgs': 0,
        })

    def run(self, argc, argv):
        self.show.show_module_targets(
            self.modules.get_current_module())
