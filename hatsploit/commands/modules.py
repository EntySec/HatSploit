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
            'Name': "modules",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - command developer',
            ],
            'Description': "Show available modules.",
        })

        self.modules = Modules()
        self.show = Show()

    def collect_categories(self):
        modules = self.modules.get_modules()
        categories = []

        if modules:
            for module in sorted(modules):
                category = modules[module]['Category']

                if category not in categories:
                    categories.append(category)

        return categories

    def rpc(self, *_):
        return self.modules.get_modules()

    def run(self, args):
        categories = self.collect_categories()

        if len(args) > 1:
            if args[1] in categories:
                self.show.show_modules(self.modules.get_modules(), args[1])
            else:
                self.print_error("Invalid module category!")
                self.print_information(f"Available categories: {', '.join(categories)}")
        else:
            self.show.show_modules(self.modules.get_modules())
