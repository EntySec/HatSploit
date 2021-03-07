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

from utils.tcp_tools import tcp_tools
from utils.web_tools import web_tools

class HatSploitModule(HatSploitModule):
    types = types()

    tcp_tools = tcp_tools()
    web_tools = web_tools()

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
        'Risk': "low"
    }

    options = {
        'RHOST': {
            'Description': "Remote host.",
            'Value': None,
            'Required': True
        },
        'RANGE': {
            'Description': "Ports to scan.",
            'Value': "0-65535",
            'Required': True
        },
        'TIMEOUT': {
            'Description': "Timeout for scan.",
            'Value': 0.5,
            'Required': True
        }
    }

    def run(self):
        remote_host, ports_range, timeout = self.parser.parse_options(self.options)
        timeout = self.types.cast_to_float(timeout)

        if timeout is None:
            return

        try:
            start = int(ports_range.split('-')[0].strip())
            end = int(ports_range.split('-')[1].strip())
        except Exception:
            self.badges.output_error("Invalid range provided!")
            return

        self.badges.output_process("Scanning " + remote_host + "...")
        for port in range(start, end):
            target = self.web_tools.format_host_and_port(remote_host, port)

            if self.tcp_tools.check_tcp_port(remote_host, port, timeout):
                self.badges.output_success(target + " - opened")
