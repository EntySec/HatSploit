#!/usr/bin/env python3

#
# This command requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.lib.command import Command
from hatsploit.lib.modules import Modules


class HatSploitCommand(Command):
    modules = Modules()

    details = {
        'Category': "modules",
        'Name': "info",
        'Authors': [
            'Ivan Nikolsky (enty8080) - command developer'
        ],
        'Description': "Show module information.",
        'Usage': "info [<module>]",
        'MinArgs': 0
    }

    def format_module_information(self, current_module):
        authors = ""
        for author in current_module['Authors']:
            authors += author + ", "
        authors = authors[:-2]

        comments = ""
        for line in current_module['Comments']:
            comments += line + "\n" + (" " * 14)
        comments = comments[:-15]

        self.print_information("Module information:")
        self.print_empty("")

        if current_module['Name']:
            self.print_empty("         Name: " + current_module['Name'])
        if current_module['Module']:
            self.print_empty("       Module: " + current_module['Module'])
        if authors:
            self.print_empty("      Authors: ")
            for author in current_module['Authors']:
                self.print_empty("               " + author)
        if current_module['Description']:
            self.print_empty("  Description: " + current_module['Description'])
        if comments:
            self.print_empty("     Comments: ")
            self.print_empty("               " + comments)
        if current_module['Risk']:
            self.print_empty("         Risk: " + current_module['Risk'])

        self.print_empty("")

    def get_module_information(self, module):
        if self.modules.check_exist(module):
            module = self.modules.get_module_object(module)
            self.format_module_information(module)
        else:
            self.print_error("Invalid module!")

    def run(self, argc, argv):
        if self.modules.check_current_module():
            if argc > 0:
                self.get_module_information(argv[0])
            else:
                self.format_module_information(self.modules.get_current_module_object().details)
        else:
            if argc > 0:
                self.get_module_information(argv[0])
            else:
                self.print_usage(self.details['Usage'])
