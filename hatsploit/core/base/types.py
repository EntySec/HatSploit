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

import re


class Types:
    platforms = {
        'generic': [
            'unix',
            'linux',
            'aix',
            'bsd',
            'macos',
            'apple_ios',
            'android',
            'windows'
        ],
        'unix': [
            'unix',
            'linux',
            'aix',
            'bsd',
            'macos',
            'apple_ios',
            'android'
        ],
        'windows': [
            'windows'
        ]
    }

    architectures = {
        'generic': [
            'x64',
            'x86',
            'aarch64',
            'armle',
            'mipsle',
            'mipsbe'
        ],
        'intel': [
            'x64',
            'x86'
        ],
        'arm': [
            'aarch64',
            'armle'
        ],
        'mips': [
            'mipsle',
            'mipsbe'
        ]
    }

    @staticmethod
    def is_mac(mac):
        regexp = r"^[a-f\d]{1,2}:[a-f\d]{1,2}:[a-f\d]{1,2}:[a-f\d]{1,2}:[a-f\d]{1,2}:[a-f\d]{1,2}$"
        if re.match(regexp, mac.lower()):
            return True
        return False

    @staticmethod
    def is_ipv4(host):
        regexp = "^(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$"
        if re.match(regexp, host):
            return True
        return False

    @staticmethod
    def is_ipv6(host):
        regexp = "^(?:(?:[0-9A-Fa-f]{1,4}:){6}(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|::(?:[0-9A-Fa-f]{1,4}:){5}(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:[0-9A-Fa-f]{1,4})?::(?:[0-9A-Fa-f]{1,4}:){4}(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4})?::(?:[0-9A-Fa-f]{1,4}:){3}(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:(?:[0-9A-Fa-f]{1,4}:){,2}[0-9A-Fa-f]{1,4})?::(?:[0-9A-Fa-f]{1,4}:){2}(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:(?:[0-9A-Fa-f]{1,4}:){,3}[0-9A-Fa-f]{1,4})?::[0-9A-Fa-f]{1,4}:(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:(?:[0-9A-Fa-f]{1,4}:){,4}[0-9A-Fa-f]{1,4})?::(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:(?:[0-9A-Fa-f]{1,4}:){,5}[0-9A-Fa-f]{1,4})?::[0-9A-Fa-f]{1,4}|(?:(?:[0-9A-Fa-f]{1,4}:){,6}[0-9A-Fa-f]{1,4})?::)%.*$"
        if re.match(regexp, host):
            return True
        return False

    def is_ip(self, value):
        if self.is_ipv4(value) or self.is_ipv6(value):
            return True
        return False

    def is_ipv4_range(self, value):
        value = value.split('/')
        if len(value) == 2:
            if self.is_ipv4(value[0]) and int(value[1]) in [8, 16, 24, 32]:
                return True
        return False

    @staticmethod
    def is_ipv6_range(value):
        # NOT IMPLEMENTED YET!
        return False

    def is_port(self, value):
        if self.is_integer(value):
            if 0 < int(value) <= 65535:
                return True
        return False

    def is_port_range(self, value):
        value = value.split('-')
        if len(value) == 2:
            if int(value[0]) <= int(value[1]):
                if self.is_port(value[0]) and self.is_port(value[1]):
                    return True
        return False

    @staticmethod
    def is_integer(value):
        value = str(value)
        if value.isdigit():
            return True
        return False

    @staticmethod
    def is_float(value):
        value = str(value)
        if re.match(r'^-?\d+(?:\.\d+)$', value):
            return True
        return False

    def is_number(self, value):
        if self.is_integer(value) or self.is_float(value):
            return True
        return False

    @staticmethod
    def is_boolean(value):
        value = value.lower()
        if value in ['yes', 'no', 'y', 'n']:
            return True
        return False
