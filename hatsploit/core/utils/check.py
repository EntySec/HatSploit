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
import sys

from hatsploit.lib.config import Config
from hatsploit.core.db.importer import Importer
from hatsploit.core.cli.badges import Badges


class Check:
    def __init__(self):
        self.config = Config()
        self.importer = Importer()
        self.badges = Badges()

    def check_modules(self):
        one_fail = False
        self.badges.output_process("Checking all base modules...")

        modules_path = os.path.normpath(self.config.path_config['modules_path'])
        for dest, _, files in os.walk(modules_path):
            for file in files:
                if file.endswith('.py') and file != '__init__.py':
                    module = dest + '/' + file[:-3]

                    try:
                        module_object = self.importer.import_module(module)
                        keys = ['Name', 'Module', 'Authors', 'Description', 'Comments', 'Platform', 'Risk']
                        assert(all(key in module_object.details for key in keys))
                        self.badges.output_success(f"{module}: OK")
                    except Exception:
                        self.badges.output_error(f"{module}: FAIL")
                        one_fail = True
        return one_fail

    def check_payloads(self):
        one_fail = False
        self.badges.output_process("Checking all base payloads...")

        payloads_path = os.path.normpath(self.config.path_config['payloads_path'])
        for dest, _, files in os.walk(payloads_path):
            for file in files:
                if file.endswith('.py') and file != '__init__.py':
                    payload = dest + '/' + file[:-3]

                    try:
                        payload_object = self.importer.import_payload(payload)
                        keys = ['Category', 'Name', 'Payload', 'Authors', 'Description',
                                'Comments', 'Architecture', 'Platform', 'Risk', 'Type']
                        assert(all(key in payload_object.details for key in keys))
                        self.badges.output_success(f"{payload}: OK")
                    except Exception:
                        self.badges.output_error(f"{payload}: FAIL")
                        one_fail = True
        return one_fail

    def check_plugins(self):
        one_fail = False
        self.badges.output_process("Checking all base plugins...")

        plugins_path = os.path.normpath(self.config.path_config['plugins_path'])
        for dest, _, files in os.walk(plugins_path):
            for file in files:
                if file.endswith('.py') and file != '__init__.py':
                    plugin = dest + '/' + file[:-3]

                    try:
                        plugin_object = self.importer.import_plugin(plugin)
                        keys = ['Name', 'Authors', 'Description', 'Comments']
                        assert(all(key in plugin_object.details for key in keys))
                        self.badges.output_success(f"{plugin}: OK")
                    except Exception:
                        self.badges.output_error(f"{plugin}: FAIL")
                        one_fail = True
        return one_fail

    def check_all(self):
        fails = list()

        fails.append(self.check_modules())
        fails.append(self.check_payloads())
        fails.append(self.check_plugins())
    
        for fail in fails:
            if fail:
                self.badges.output_error("Not all checks passed!")
                return False
        self.badges.output_success("All checks passed!")
        return True
