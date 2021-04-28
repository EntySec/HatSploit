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

from core.base.storage import LocalStorage
from core.cli.badges import Badges
from core.db.importer import Importer
from core.payloads.payloads import Payloads


class PayloadsChecks:
    def __init__(self):
        self.badges = Badges()
        self.importer = Importer()
        self.local_storage = LocalStorage()
        self.payloads = Payloads()

    def perform_check(self):
        fail = False
        all_payloads = self.local_storage.get("payloads")
        if all_payloads:
            for database in all_payloads.keys():
                self.badges.output_process("Checking payloads from " + database + " database...")
                payloads = all_payloads[database]
                for platform in payloads.keys():
                    for architecture in payloads[platform].keys():
                        for payload in payloads[platform][architecture].keys():
                            try:
                                _ = self.importer.import_payload(payloads[platform][architecture][payload]['Path'])
                                self.badges.output_success(
                                    self.payloads.get_full_name(platform, architecture, payload) + ': OK')
                            except Exception:
                                self.badges.output_error(
                                    self.payloads.get_full_name(platform, architecture, payload) + ': FAIL')
                                fail = True
        return fail
