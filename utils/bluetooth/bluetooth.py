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

import struct

from core.cli.badges import Badges
from bluepy.btle import Scanner, DefaultDelegate
from bluepy.btle import Peripheral, ScanEntry, AssignedNumbers


class ScanDelegate(DefeultDelegate):
    def __init__(self, mac, buffering=False, enumeration=False):
        DefaultDelegate.__init__(self)
        self.mac = mac
        self.buffering = buffering
        self.enumeration = enumeration

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if not isNewDev:
            return
        elif self.mac and dev.addr != self.mac:
            return

        if self.buffering:
            dev.print_info()

class BluetoothDevice(ScanEntry):
    badges = Badges()


class BluetoothScanner(Scanner):
    badges = Badges()


class BluetoothClient:
    badges = Badges()

    def ble_scan(self, mac=None, buffering=False, enumeration=False, timeout=10):
        scanner = BluetoothScanner(mac).withDelegate(ScanDelegate(mac, buffering, enumeration))

        if mac is not None:
            self.badges.output_process("Scanning BLE device...")
        else:
            self.badges.output_process("Scanning for BLE devices...")

        devices = list()
        try:
            devices = [result for result in scanner.scan(timeout)]
        except Exception as e:
            self.badges.output_error("Failed to scan. Check your bluetooth hardware.")
            self.badges.output_information(f"Trace: {str(e)}")

        return devices
