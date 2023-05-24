"""
This command requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.command import Command
from hatsploit.lib.modules import Modules
from hatsploit.lib.show import Show


class HatSploitCommand(Command):
    def __init__(self):
        super().__init__()

        self.modules = Modules()
        self.show = Show()

        self.details.update({
            'Category': "modules",
            'Name': "info",
            'Authors': [
                'Ivan Nikolsky (enty8080) - command developer',
            ],
            'Description': "Show module information.",
            'Usage': "info [<module>]",
            'MinArgs': 0,
        })

        self.complete = self.modules.modules_completer

    def get_module_information(self, module):
        if self.modules.check_exist(module):
            module = self.modules.get_module_object(module)
            self.show.show_module_information(module)
        else:
            self.print_error("Invalid module!")

    def run(self, argc, argv):
        if self.modules.get_current_module():
            if argc > 1:
                self.get_module_information(argv[1])
            else:
                self.show.show_module_information(
                    None
                )
        else:
            if argc > 1:
                self.get_module_information(argv[1])
            else:
                self.print_usage(self.details['Usage'])
