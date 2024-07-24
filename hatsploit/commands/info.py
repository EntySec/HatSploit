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
            'Name': "info",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - command developer',
            ],
            'Description': "Show module information.",
            'Usage': "info [<module>]",
            'MinArgs': 0,
        })

        self.modules = Modules()
        self.show = Show()
        self.complete = self.modules.modules_completer()

    def get_module_information(self, module):
        if self.modules.check_exist(module):
            module = self.modules.get_module_object(module)
            self.show.show_module_information(module)
        else:
            self.print_error("Invalid module!")

    def run(self, args):
        if self.modules.get_current_module():
            if len(args) > 1:
                self.get_module_information(args[1])
            else:
                self.show.show_module_information(
                    None
                )
        else:
            if len(args) > 1:
                self.get_module_information(args[1])
            else:
                self.print_usage(self.info['Usage'])
