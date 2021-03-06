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

import scapy.all

from core.cli.badges import badges
from core.cli.parser import parser
from core.cli.tables import tables
from core.base.types import types

class HatSploitModule:
    def __init__(self):
        self.badges = badges()
        self.parser = parser()
        self.tables = tables()
        self.types = types()
        
        self.details = {
            'Name': "Network Scanner",
            'Module': "auxiliary/multi/scanner/network_scanner",
            'Authors': [
                'enty8080'
            ],
            'Description': "Scan local network.",
            'Dependencies': [
                'scapy'
            ],
            'Comments': [
                'Uses Python scapy module to scan local network.'
            ],
            'Risk': "low"
        }

        self.options = {
            'RANGE': {
                'Description': "IP range.",
                'Value': "192.168.1.1/24",
                'Required': True
            },
            'TIMEOUT': {
                'Description': "Timeout to scan.",
                'Value': 10,
                'Required': True
            }
        }

    def run(self):
        ip_range, timeout = self.parser.parse_options(self.options)
        timeout = self.types.cast_to_float(timeout)
        
        if timeout == None:
            return
        
        self.badges.output_process("Scanning local network...")
        
        try:
            arp = scapy.all.ARP(pdst=ip_range)
            ether = scapy.all.Ether(dst="ff:ff:ff:ff:ff:ff")
            result = scapy.all.srp(ether/arp, timeout=timeout, verbose=False)[0]
        
            if len(result) > 0:
                net_data = list()
                headers = ("Host", "MAC")
                for _, received in result:
                    net_data.append((received.psrc, received.hwsrc))
                self.badges.output_empty("")
                self.tables.print_table("Network Devices", headers, *net_data)
                self.badges.output_empty("")
            else:
                self.badges.output_warning("No hosts detected in local network.")
        except Exception:
            self.badges.output_error("Failed to scan local network!")
