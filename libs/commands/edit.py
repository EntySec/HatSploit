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

import os

from core.lib.command import HatSploitCommand

from core.modules.modules import modules
from core.base.storage import local_storage

class HatSploitCommand(HatSploitCommand):
    modules = modules()
    local_storage = local_storage()

    details = {
        'Category': "developer",
        'Name': "edit",
        'Authors': [
            'enty8080'
        ],
        'Description': "Open module in editor.",
        'Usage': "edit <module>",
        'MinArgs': 1
    }

    def run(self, argc, argv):
        module = argv[0]
        
        module_category = self.modules.get_category(module)
        module_platform = self.modules.get_platform(module)
        module_name = self.modules.get_name(module)
        
        try:
            if not os.environ['EDITOR']:
                self.badges.output_warning("Shell variable EDITOR not set.")
                editor = "vi"
            else:
                editor = os.environ['EDITOR']
        except KeyError:
            self.badges.output_warning("Shell variable EDITOR not set.")
            editor = "vi"
            
        if self.modules.check_exist(module):
            if not self.modules.check_imported(module):
                database = self.modules.get_database(module)
                module_path = self.local_storage.get("modules")[database][module_category][module_platform][module_name]['Path']
                edit_mode = editor + " " + self.config.path_config['base_paths']['root_path'] + module_path
                self.execute.execute_system(edit_mode)
            else:
                self.badges.output_error("Can not edit already used module!")
        else:
            self.badges.output_error("Invalid module!")
