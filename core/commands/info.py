#!/usr/bin/env python3

#
# MIT License
#
# Copyright (c) 2020-2021 EntySec
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

from core.lib.command import Command

from core.modules.modules import Modules


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
            category = self.modules.get_category(module)
            platform = self.modules.get_platform(module)
            name = self.modules.get_name(module)

            module = self.modules.get_module_object(category, platform, name)
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
