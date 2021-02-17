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

from core.badges import badges
from core.storage import local_storage

class modules:
    def __init__(self):
        self.badges = badges()
        self.local_storage = local_storage()
        
    def check_exist(self, name):
        if self.check_style(name):
            all_modules = self.local_storage.get("modules")
            if all_modules:
                for database in all_modules.keys():
                    modules = all_modules[database]
                
                    category = self.get_category(name)
                    platform = self.get_platform(name)
        
                    if category in modules.keys():
                        if platform in modules[category].keys():
                            module = self.get_name(name)
                            if module in modules[category][platform].keys():
                                return True
        return False

    def check_imported(self, name):
        imported_modules = self.local_storage.get("imported_modules")
        if imported_modules:
            if name in imported_modules.keys():
                return True
        return False
    
    def check_style(self, name):
        if len(name.split('/')) >= 4:
            return True
        return False
    
    def check_current_module(self):
        if self.local_storage.get("current_module"):
            if len(self.local_storage.get("current_module")) > 0:
                return True
        return False
    
    def get_module_object(self, category, platform, name):
        module_full_name = self.get_full_name(category, platform, name)
        if self.check_exist(module_full_name):
            database = self.get_database(module_full_name)
            return self.local_storage.get("modules")[database][category][platform][name]
        return None
    
    def get_current_module_object(self):
        if self.check_current_module():
            return self.local_storage.get_array("current_module", self.local_storage.get("current_module_number"))
        return None
    
    def get_current_module_name(self):
        if self.check_current_module():
            return self.local_storage.get_array("current_module", self.local_storage.get("current_module_number")).details['Name']
        return None
       
    def get_database(self, name):
        if self.check_style(name):
            all_modules = self.local_storage.get("modules")
            if all_modules:
                for database in all_modules.keys():
                    modules = all_modules[database]
                
                    category = self.get_category(name)
                    platform = self.get_platform(name)
        
                    if category in modules.keys():
                        if platform in modules[category].keys():
                            module = self.get_name(name)
                            if module in modules[category][platform].keys():
                                return database
        return None
        
    def get_category(self, name):
        if self.check_style(name):
            return name.split('/')[0]
        return None

    def get_platform(self, name):
        if self.check_style(name):
            return name.split('/')[1]
        return None
    
    def get_name(self, name):
        if self.check_style(name):
            return os.path.join(*(name.split(os.path.sep)[2:]))
        return None

    def get_full_name(self, category, platform, name):
        return category + '/' + platform + '/' + name
