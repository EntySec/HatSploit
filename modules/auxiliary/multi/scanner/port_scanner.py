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

from core.lib.module import HatSploitModule
from core.base.types import types

from utils.tcp.tcp import tcp
from utils.http.http import http

class HatSploitModule(HatSploitModule):
    types = types()

    tcp = tcp()
    http = http()

    details = {
        'Name': "Port Scanner",
        'Module': "auxiliary/multi/scanner/port_scanner",
        'Authors': [
            'enty8080'
        ],
        'Description': "Scan host for opened ports.",
        'Dependencies': [
            ''
        ],
        'Comments': [
            ''
        ],
        'Platform': "multi",
        'Risk': "low"
    }

    options = {
        'RHOST': {
            'Description': "Remote host.",
            'Value': None,
            'Type': "ip",
            'Required': True
        },
        'RANGE': {
            'Description': "Ports to scan.",
            'Value': "0-65535",
            'Type': "port_range",
            'Required': True
        },
        'TIMEOUT': {
            'Description': "Timeout for scan.",
            'Value': 0.5,
            'Type': "number",
            'Required': True
        }
    }

    def run(self):
        remote_host, ports_range, timeout = self.parser.parse_options(self.options)

        start = int(ports_range.split('-')[0].strip())
        end = int(ports_range.split('-')[1].strip())

        self.badges.output_process("Scanning " + remote_host + "...")
        for port in range(start, end):
            target = self.http.format_host_and_port(remote_host, port)

            if self.tcp.check_tcp_port(remote_host, port, float(timeout)):
                self.badges.output_success(target + " - opened")
