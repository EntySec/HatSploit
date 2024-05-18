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
            'Name': "modules",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - command developer',
            ],
            'Description': "Show available modules.",
            'Usage': "modules [category]",
            'MinArgs': 0,
        })

    def collect_categories(self):
        modules = self.modules.get_modules()
        categories = []

        if modules:
            for database in sorted(modules):
                for module in sorted(modules[database]):
                    category = modules[database][module]['Category']

                    if category not in categories:
                        categories.append(category)

        return categories

    def rpc(self, *args):
        return self.modules.get_modules()

    def run(self, argc, argv):
        categories = self.collect_categories()

        if argc > 1:
            if argv[1] in categories:
                self.show.show_modules(self.modules.get_modules(), argv[1])
            else:
                self.print_error("Invalid module category!")
                self.print_information(f"Available categories: {str(categories)}")
        else:
            self.show.show_modules(self.modules.get_modules())
