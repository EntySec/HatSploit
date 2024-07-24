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
            'Name': "use",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - command developer',
            ],
            'Description': "Use specified module.",
            'Usage': "use <module|number>",
            'MinArgs': 1,
        })

        self.modules = Modules()
        self.complete = self.modules.modules_completer()

    def rpc(self, *args):
        if len(args) < 1:
            return

        self.modules.use_module(args[0])

    def run(self, args):
        module = self.modules.get_current_module()

        if module:
            for command in module.commands:
                self.console.delete_external(command)

        self.modules.use_module(args[1])

        module = self.modules.get_current_module()
        commands = {}

        for command in module.commands:
            commands[command] = module.commands[command]
            commands[command]['Method'] = getattr(module, command)
            commands[command]['Category'] = 'module'

        self.console.add_external(commands)
