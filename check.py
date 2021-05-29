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

from core.base.config import Config

config = Config()
config.configure()

from core.db.importer import Importer
from core.cli.badges import Badges

importer = Importer()
badges = Badges()

def check_modules():
    one_fail = False
    self.badges.output_process("Checking all stdalone modules...")

    modules_path = 'modules'
    for dest, _, files in os.walk(modules_path):
        for file in files:
            if file.endswith('.py') and file != '__init__.py':
                module = dest + '/' + file[:-3]
                module_name = module[len(f"{modules_path}/"):]

                try:
                    _ = importer.import_payload(payload)
                    badges.output_success(f"{module_name}: OK")
                except Exception:
                    badges.output_error(f"{module_name}: FAIL")
                    one_fail = True
    return one_fail

