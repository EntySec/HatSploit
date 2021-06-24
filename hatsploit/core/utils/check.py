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

from hatsploit.base.config import Config
from hatsploit.core.db.importer import Importer
from hatsploit.core.cli.badges import Badges


class Check:
    def __init__(self):
        self.config = Config()
        self.importer = Importer()
        self.badges = Badges()

    def check_modules(self):
        one_fail = False
        self.badges.output_process("Checking all stdalone modules...")

        modules_path = os.path.split(
            self.config.path_config['modules_path']
        )[0]
        for dest, _, files in os.walk(modules_path):
            for file in files:
                if file.endswith('.py') and file != '__init__.py':
                    module = dest + '/' + file[:-3]
                    module_name = module[len(f"{modules_path}/"):]

                    try:
                        module_object = self.importer.import_module(module)
                        keys = ['Name', 'Module', 'Authors', 'Description', 'Comments', 'Platform', 'Risk']
                        assert(all(key in module_object.details for key in keys))
                        self.badges.output_success(f"{module_name}: OK")
                    except Exception:
                        self.badges.output_error(f"{module_name}: FAIL")
                        one_fail = True
        return one_fail

    def check_payloads(self):
        one_fail = False
        self.badges.output_process("Checking all stdalone payloads...")

        payloads_path = os.path.split(
            self.config.path_config['payloads_path']
        )[0]
        for dest, _, files in os.walk(payloads_path):
            for file in files:
                if file.endswith('.py') and file != '__init__.py':
                    payload = dest + '/' + file[:-3]
                    payload_name = payload[len(f"{payloads_path}/"):]

                    try:
                        payload_object = self.importer.import_payload(payload)
                        keys = ['Category', 'Name', 'Payload', 'Authors', 'Description',
                                'Comments', 'Architecture', 'Platform', 'Risk', 'Type']
                        assert(all(key in payload_object.details for key in keys))
                        self.badges.output_success(f"{payload_name}: OK")
                    except Exception:
                        self.badges.output_error(f"{payload_name}: FAIL")
                        one_fail = True
        return one_fail

    def check_plugins(self):
        one_fail = False
        self.badges.output_process("Checking all stdalone plugins...")

        plugins_path = os.path.split(
            self.config.path_config['plugins_path']
        )[0]
        for dest, _, files in os.walk(plugins_path):
            for file in files:
                if file.endswith('.py') and file != '__init__.py':
                    plugin = dest + '/' + file[:-3]
                    plugin_name = plugin[len(f"{plugins_path}/"):]

                    try:
                        plugin_object = self.importer.import_plugin(plugin)
                        keys = ['Name', 'Authors', 'Description', 'Comments']
                        assert(all(key in plugin_object.details for key in keys))
                        self.badges.output_success(f"{plugin_name}: OK")
                    except Exception:
                        self.badges.output_error(f"{plugin_name}: FAIL")
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
