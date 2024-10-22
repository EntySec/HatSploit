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
            'Name': "unload",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - command developer',
            ],
            'Description': "Unload specified loaded plugin.",
            'Usage': "unload <plugin|number>",
            'MinArgs': 1,
        })

        self.plugins = Plugins()

    def complete(self):
        return self.plugins.loaded_plugins_completer()

    def run(self, args):
        plugin = self.plugins.get_loaded_plugins().get(args[1], None)

        if not plugin:
            self.print_error(f"Plugin is not loaded: {args[1]}!")
            return

        for command in plugin.commands:
            self.console.delete_external(command)

        self.plugins.unload_plugin(args[1])
