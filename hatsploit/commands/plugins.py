"""
This command requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.command import Command
from hatsploit.lib.plugins import Plugins
from hatsploit.lib.show import Show


class HatSploitCommand(Command):
    def __init__(self):
        super().__init__()

        self.show = Show()
        self.plugins = Plugins()

        self.details.update({
            'Category': "plugins",
            'Name': "plugins",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - command developer',
            ],
            'Description': "Show available plugins.",
            'Usage': "plugins",
            'MinArgs': 0,
        })

    def rpc(self, *args):
        return self.plugins.get_plugins()

    def run(self, argc, argv):
        self.show.show_plugins(self.plugins.get_plugins())
