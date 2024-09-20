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
            'Name': "show",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - command developer',
            ],
            'Description': "Show current module criteria.",
            'Usage': "show [options|advanced|targets|devices]",
            'MinArgs': 1,
        })

        self.modules = Modules()

    def run(self, args):
        if args[1] == 'advanced':
            Show().show_advanced(self.modules.get_current_module())
        elif args[1] == 'options':
            Show().show_options(self.modules.get_current_module())
        elif args[1] == 'targets':
            Show().show_module_targets(self.modules.get_current_module())
        elif args[1] == 'devices':
            Show().show_module_devices(self.modules.get_current_module())
        else:
            self.print_usage(self.info['Usage'])
