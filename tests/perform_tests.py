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

import sys

from core.cli.badges import Badges
from core.db.importer import Importer
from tests.modules_tests import ModulesTests
from tests.payloads_tests import PayloadsTests
from tests.plugins_tests import PluginsTests


class PerformTests:
    def __init__(self):
        self.badges = Badges()
        self.importer = Importer()

        self.modules_tests = ModulesTests()
        self.plugins_tests = PluginsTests()
        self.payloads_tests = PayloadsTests()

    def perform_tests(self):
        self.importer.import_database()

        statuses = list()
        self.badges.output_process("Performing modules test...")
        statuses.append(self.modules_tests.perform_test())

        self.badges.output_process("Performing plugins test...")
        statuses.append(self.plugins_tests.perform_test())

        self.badges.output_process("Performing payloads test...")
        statuses.append(self.payloads_tests.perform_test())

        for status in statuses:
            if status:
                self.badges.output_error("Not all tests passed!")
                sys.exit(1)
        self.badges.output_success("All tests passed!")
