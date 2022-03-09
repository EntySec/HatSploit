#!/usr/bin/env python3

#
# This command requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.lib.command import Command
from hatsploit.lib.payloads import Payloads
from hatsploit.lib.show import Show


class HatSploitCommand(Command):
    payloads = Payloads()
    show = Show()

    details = {
        'Category': "modules",
        'Name': "payloads",
        'Authors': [
            'Ivan Nikolsky (enty8080) - command developer'
        ],
        'Description': "Show available payloads.",
        'Usage': "payloads [category]",
        'MinArgs': 0
    }

    def collect_categories(self):
        payloads = self.payload.get_payloads()
        categories = []

        if payloads:
            for database in sorted(payloads):
                for payload in sorted(payloads[database]):
                    category = payloads[database][payload]['Category']

                    if category not in categories:
                        categories.append(category)

        return categories

    def run(self, argc, argv):
        categories = self.collect_categories()

        if argc > 1:
            if argv[1] in categories:
                self.show.show_payloads(argv[1])
            else:
                self.print_error("Invalid payload category!")
                self.print_information(f"Available categories: {str(categories)}")
        else:
            self.show.show_payloads()
