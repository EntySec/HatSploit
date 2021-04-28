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
from checks.modules_checks import ModulesChecks
from checks.payloads_checks import PayloadsChecks
from checks.plugins_checks import PluginsChecks


class PerformChecks:
    def __init__(self):
        self.badges = Badges()
        self.importer = Importer()

        self.modules_checks = ModulesChecks()
        self.plugins_checks = PluginsChecks()
        self.payloads_checks = PayloadsChecks()

    def perform_checks(self):
        self.importer.import_database()

        statuses = list()
        self.badges.output_process("Performing modules check...")
        statuses.append(self.modules_checks.perform_check())

        self.badges.output_process("Performing plugins check...")
        statuses.append(self.plugins_checks.perform_check())

        self.badges.output_process("Performing payloads check...")
        statuses.append(self.payloads_checks.perform_check())

        for status in statuses:
            if status:
                self.badges.output_error("Not all checks passed!")
                sys.exit(1)
        self.badges.output_success("All checks passed!")
