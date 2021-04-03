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

from core.lib.module import Module
from utils.bluetooth.bluetooth import BluetoothClient

class HatSploitModule(Module, BluetoothClient):
    details = {
        'Name': "Bluetooth Low Energy Enumerate",
        'Module': "auxiliary/multi/enumerate/ble_enumerate",
        'Authors': [
            'Ivan Nikolsky (enty8080)'
        ],
        'Description': "Enumerate bluetooth low energy devices characteristics.",
        'Dependencies': [
            'bluepy'
        ],
        'Comments': [
            ''
        ],
        'Platform': "multi",
        'Risk': "high"
    }

    options = {
        'MAC': {
            'Description': "MAC address.",
            'Value': None,
            'Type': "mac",
            'Required': True
        }
    }

    def run(self):
        mac = self.parse_options(self.options)

        result = self.btle_scan(self.target)
        if result:
            device = result[0]
            device.print_services()
