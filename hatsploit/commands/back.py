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
        })

        self.modules = Modules()

    def rpc(self, *_):
        self.modules.go_back()

    def run(self, _):
        module = self.modules.get_current_module()

        if not module:
            return

        self.console.delete_external(module.commands)
        self.modules.go_back()

        module = self.modules.get_current_module()

        if module:
            for command in module.commands:
                command.info['Method'] = getattr(module, command.info['Name'])
                command.info['Category'] = 'module'

            self.console.add_external(module.commands)
