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

from core.badges import badges
from core.importer import importer

from tests.modules_tests import modules_tests
from tests.plugins_tests import plugins_tests

class perform_tests:
    def __init__(self):
        self.badges = badges()
        self.importer = importer()

        self.modules_tests = modules_tests()
        self.plugins_tests = plugins_tests()
        
    def perform_tests(self):
        self.importer.import_database()
        
        statuses = list()
        self.badges.output_process("Performing modules test...")
        statuses.append(self.modules_tests.perform_test())
        
        self.badges.output_process("Performing plugins test...")
        statuses.append(self.plugins_tests.perform_test())
        
        for status in statuses:
            if status:
                self.badges.output_error("Not all tests passed!")
                sys.exit(1)
        self.badges.output_success("All tests passed!")
