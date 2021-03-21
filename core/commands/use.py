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

from core.base.storage import LocalStorage
from core.db.importer import Importer
from core.lib.command import Command
from core.modules.modules import Modules


class HatSploitCommand(Command):
    importer = Importer()
    local_storage = LocalStorage()
    modules = Modules()

    details = {
        'Category': "module",
        'Name': "use",
        'Authors': [
            'enty8080'
        ],
        'Description': "Use specified module.",
        'Usage': "use <module>",
        'MinArgs': 1
    }

    def check_if_already_used(self, module):
        if self.modules.check_current_module():
            if module == self.modules.get_current_module_name():
                return True
        return False

    def run(self, argc, argv):
        module = argv[0]

        category = self.modules.get_category(module)
        platform = self.modules.get_platform(module)
        name = self.modules.get_name(module)

        if not self.check_if_already_used(module):
            if self.modules.check_exist(module):
                self.modules.add_module(category, platform, name)
            else:
                self.output_error("Invalid module!")
