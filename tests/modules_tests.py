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
from core.importer import importer
from core.storage import local_storage
from core.modules import modules

class modules_tests:
    def __init__(self):
        self.badges = badges()
        self.importer = importer()
        self.local_storage = local_storage()
        self.modules = modules()
        
    def perform_test(self):
        fail = False
        all_modules = self.local_storage.get("modules")
        if all_modules:
            for database in all_modules.keys():
                self.badges.output_process("Testing modules from " + database + " database...")
                modules = all_modules[database]
                for category in modules.keys():
                    for platform in modules[category].keys():
                        for module in modules[category][platform].keys():
                            try:
                                _ = self.importer.import_module(modules[category][platform][module]['Path'])
                                self.badges.output_success(self.modules.get_full_name(category, platform, module) + ': OK')
                            except Exception:
                                self.badges.output_error(self.modules.get_full_name(category, platform, module) + ': FAIL')
                                fail = True
        return fail
