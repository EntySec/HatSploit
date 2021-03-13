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

from core.base.storage import local_storage

class payloads:
    def __init__(self):
        self.local_storage = local_storage()

    def check_exist(self, name):
        if self.check_style(name):
            all_payloads = self.local_storage.get("payloads")
            if all_payloads:
                for database in all_payloads.keys():
                    payloads = all_payloads[database]

                    platform = self.get_platform(name)
                    architecture = self.get_architecture(nane)

                    if platform in payloads.keys():
                        if architecture in payloads[platform].keys():
                            payload = self.get_name(name)
                            if payload in payloads[platform][architecture].keys():
                                return True
        return False

    def check_style(self, name):
        if len(name.split('/')) >= 3:
            return True
        return False

    def get_platform(self, name):
        if self.check_style(name):
            return name.split('/')[0]
        return None

    def get_architecture(self, name):
        if self.check_style(name):
            return name.split('/')[1]
        return None

    def get_name(self, name):
        if self.check_style(name):
            return os.path.join(*(name.split(os.path.sep)[2:]))
        return None

    def get_payload_object(self, platform, architecture, name):
        payload_full_name = self.get_full_name(platform, architecture, name)
        if self.check_exist(payload_full_name):
            database = self.get_database(payload_full_name)
            return self.local_storage.get("payloads")[database][platform][architecture][name]
        return None

    def check_exist(self, name):
        if self.check_style(name):
            all_payloads = self.local_storage.get("payloads")
            if all_payloads:
                for database in all_payloads.keys():
                    payloads = all_payloads[database]

                    platform = self.get_platform(name)
                    architecture = self.get_architecture(nane)

                    if platform in payloads.keys():
                        if architecture in payloads[platform].keys():
                            payload = self.get_name(name)
                            if payload in payloads[platform][architecture].keys():
                                return database
        return None

    def get_full_name(self, platform, architecture, name):
        return platform + '/' + architecture + '/' + name
