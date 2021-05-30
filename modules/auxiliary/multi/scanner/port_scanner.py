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

import time
import threading

from core.lib.module import Module
from utils.tcp.tcp import TCPClient


class HatSploitModule(Module, TCPClient):
    details = {
        'Name': "Port Scanner",
        'Module': "auxiliary/multi/scanner/port_scanner",
        'Authors': [
            'Ivan Nikolsky (enty8080)'
        ],
        'Description': "Scan host for opened ports.",
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
        }
    }

    def check_port(self, remote_host, port):
        target = remote_host + '/' + str(port)
        if self.check_tcp_port(remote_host, port):
            self.output_success(f"{target} - opened")

    def run(self):
        remote_host, ports_range = self.parse_options(self.options)
        start, end = self.parse_ports_range(ports_range)

        self.output_process(f"Scanning {remote_host}...")
        for port in range(start, end):
            time.sleep(0.01) # cool down

            thread = threading.Thread(target=self.check_port, args=[remote_host, port])
            thread.start()
