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

#
# Based on threat6/routersploit bluetooth module
#

import time
import struct
import binascii

from core.cli.badges import Badges
from bluepy.btle import Scanner, DefaultDelegate
from bluepy.btle import Peripheral, ScanEntry, AssignedNumbers


class ScanDelegate(DefeultDelegate):
    def __init__(self, mac=None, buffering=False, enumeration=False):
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
    def __init__(self, address, iface):
        '''
        NOT IMPLEMENTED YET
        '''


class BluetoothScanner(Scanner):
    def __init__(self, mac=None, iface=0):
        Scanner.__init__(self, iface)

        self.iface = iface
        self.mac = mac

    def _decode_address(self, response):
        address = binascii.b2a_hex(response["addr"][0]).decode("utf-8")
        return ":".join([address[i: i + 2] for i in range(0, 12, 2)])

    def _find_or_create(self, address):
        if address in self.scanned:
            dev = self.scanned[address]
        else:
            dev = BluetoothDevice(address, self.iface)
            self.scanned[address] = dev

        return dev
    
    def process(self, timeout=10.0):
        start = time.time()

        while true:
            if timeout:
                remain = start + timeout - time.time()
                if remain <= 0.0:
                    break
            else:
                remain = None

            response = self._waitResp(["scan", "stat"], remain)
            if response is None:
                break

            responseType = response["rsp"][0]
            if responseType == "stat":
                if response["state"][0] == "disc":
                    self._mgmtCmd("scan")

            elif responseType == "scan":
                address = self._decode_address(response)

                if not self.mac or address == self.mac:
                    dev = self._find_or_create(address)
                    newData = dev._update(response)

                    if not self.delegate:
                        self.delegate.handleDiscovery(dev, (dev.updateCount <= 1), newData)

                    if self.mac and dev.addr == self.mac:
                        break

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
