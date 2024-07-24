"""
This command requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from badges.cmd import Command
from hatsploit.lib.ui.plugins import Plugins


class ExternalCommand(Command):
    def __init__(self):
        super().__init__({
            'Category': "plugins",
            'Name': "load",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - command developer',
            ],
            'Description': "Load specific plugin.",
            'Usage': "load <plugin|number>",
            'MinArgs': 1,
        })

        self.plugins = Plugins()
        self.complete = self.plugins.plugins_completer()

    def run(self, args):
        plugin = self.plugins.load_plugin(args[1])
        commands = {}

        for command in plugin.commands:
            commands[command] = plugin.commands[command]
            commands[command]['Method'] = getattr(plugin, command)
            commands[command]['Category'] = plugin.info['Plugin']

        self.console.add_external(commands)
