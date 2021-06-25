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
        'Category': "module",
        'Name': "info",
        'Authors': [
            'Ivan Nikolsky (enty8080)'
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

        self.output_information("Module information:")
        self.output_empty("")

        if current_module['Name']:
            self.output_empty("         Name: " + current_module['Name'])
        if current_module['Module']:
            self.output_empty("       Module: " + current_module['Module'])
        if authors:
            self.output_empty("      Authors: " + authors)
        if current_module['Description']:
            self.output_empty("  Description: " + current_module['Description'])
        if comments:
            self.output_empty("     Comments: ")
            self.output_empty("               " + comments)
        if current_module['Risk']:
            self.output_empty("         Risk: " + current_module['Risk'])

        self.output_empty("")

    def get_module_information(self, module):
        if self.modules.check_exist(module):
            module = self.modules.get_module_object(module)
            self.format_module_information(module)
        else:
            self.output_error("Invalid module!")

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
                self.output_usage(self.details['Usage'])
