"""
This command requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from badges.cmd import Command
from hatsploit.lib.ui.plugins import Plugins
from hatsploit.lib.ui.show import Show


class ExternalCommand(Command):
    def __init__(self):
        super().__init__({
            'Category': "plugins",
            'Name': "plugins",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - command developer',
            ],
            'Description': "Show available plugins.",
            'Usage': "plugins",
            'MinArgs': 0,
        })

        self.show = Show()
        self.plugins = Plugins()

    def rpc(self, *_):
        return self.plugins.get_plugins()

    def run(self, _):
        self.show.show_plugins(self.plugins.get_plugins())
