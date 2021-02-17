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

class plugins_tests:
    def __init__(self):
        self.badges = badges()
        self.importer = importer()
        self.local_storage = local_storage()
        
    def perform_test(self):
        fail = False
        all_plugins = self.local_storage.get("plugins")
        if all_plugins:
            for database in all_plugins.keys():
                self.badges.output_process("Testing plugins from " + database + " database...")
                plugins = all_plugins[database]
                for plugin in plugins.keys():
                    try:
                        _ = self.importer.import_plugin(plugins[plugin]['Path'])
                        self.badges.output_success(plugin + ': OK')
                    except Exception:
                        self.badges.output_error(plugin + ': FAIL')
                        fail = True
        return fail
