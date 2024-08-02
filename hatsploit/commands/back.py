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
            'Name': "back",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - command developer',
            ],
            'Description': "Return to the previous module.",
            'Usage': "back",
            'MinArgs': 0,
        })

        self.modules = Modules()

    def rpc(self, *_):
        self.modules.go_back()

    def run(self, _):
        module = self.modules.get_current_module()

        if not module:
            return

        for command in module.commands:
            self.console.delete_external(command)

        self.modules.go_back()

        module = self.modules.get_current_module()

        if module:
            commands = {}

            for command in module.commands:
                commands[command] = module.commands[command]
                commands[command]['Method'] = getattr(module, command)
                commands[command]['Category'] = 'module'

            self.console.add_external(commands)
