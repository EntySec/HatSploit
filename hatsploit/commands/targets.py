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
            'Name': "targets",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - command developer',
            ],
            'Description': "Display available module targets.",
            'Usage': "targets",
            'MinArgs': 0,
        })

        self.modules = Modules()
        self.show = Show()

    def run(self, _):
        self.show.show_module_targets(
            self.modules.get_current_module())
