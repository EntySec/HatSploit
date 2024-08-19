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

    def complete(self):
        return self.modules.modules_completer()

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

        for command in module.commands:
            command.info['Method'] = getattr(module, command.info['Name'])
            command.info['Category'] = 'module'

        self.console.add_external(module.commands)
