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

from core.templates.command import HatSploitCommand

from core.db.importer import importer
from core.base.storage import local_storage
from core.modules.modules import modules

class HatSploitCommand(HatSploitCommand):
    importer = importer()
    local_storage = local_storage()
    modules = modules()

    details = {
        'Category': "module",
        'Name': "use",
        'Description': "Use specified module.",
        'Usage': "use <module>",
        'MinArgs': 1
    }
        
    def import_module(self, category, platform, name):
        modules = self.modules.get_module_object(category, platform, name)
        try:
            module_object = self.importer.import_module(modules['Path'])
            if not self.local_storage.get("imported_modules"):
                self.local_storage.set("imported_modules", dict())
            self.local_storage.update("imported_modules", {self.modules.get_full_name(category, platform, name): module_object})
        except Exception:
            return None
        return module_object
        
    def add_module(self, category, platform, name):
        modules = self.modules.get_module_object(category, platform, name)
        
        not_installed = list()
        for dependence in modules['Dependencies']:
            if not self.importer.import_check(dependence):
                not_installed.append(dependence)
        if not not_installed:
            imported_modules = self.local_storage.get("imported_modules")
            full_name = self.modules.get_full_name(category, platform, name)
            
            if self.modules.check_imported(full_name):
                module_object = imported_modules[full_name]
                self.add_to_global(module_object)
            else:
                module_object = self.import_module(category, platform, name)
                if module_object:
                    self.add_to_global(module_object)
                else:
                    self.badges.output_error("Failed to select module from database!")
        else:
            self.badges.output_error("Module depends this dependencies which is not installed:")
            for dependence in not_installed:
                self.badges.output_empty("    * " + dependence)
                
    def add_to_global(self, module_object):
        if self.modules.check_current_module():
            self.local_storage.add_array("current_module", '')
            self.local_storage.set("current_module_number", self.local_storage.get("current_module_number") + 1)
            self.local_storage.set_array("current_module", self.local_storage.get("current_module_number"), module_object)
        else:
            self.local_storage.set("current_module", [])
            self.local_storage.set("current_module_number", 0)
            self.local_storage.add_array("current_module", '')
            self.local_storage.set_array("current_module", self.local_storage.get("current_module_number"), module_object)

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
                self.add_module(category, platform, name)
            else:
                self.badges.output_error("Invalid module!")
