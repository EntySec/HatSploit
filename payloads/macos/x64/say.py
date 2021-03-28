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

import struct

from core.lib.payload import Payload
from utils.payload.payload import PayloadGenerator


class HatSploitPayload(Payload, PayloadGenerator):
    details = {
        'Category': "stager",
        'Name': "macOS x64 Say",
        'Payload': "macos/x64/say",
        'Authors': [
            'enty8080'
        ],
        'Description': "Say payload for macOS x64.",
        'Dependencies': [
            ''
        ],
        'Comments': [
            ''
        ],
        'Architecture': "x64",
        'Platform': "macos",
        'Risk': "low",
        'Type': "one_side"
    }

    options = {
        'MESSAGE': {
            'Description': "Message to say.",
            'Value': "Hello, Friend!",
            'Type': None,
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
        message, executable_format = self.parse_options(self.options)

        message = (message + '\x00').encode()
        call = b'\xe8' + struct.pack("<I", len(message) + 0xd)

        if executable_format not in self.formats.keys():
            self.output_error("Invalid executable format!")
            return

        self.output_process("Generating shellcode...")
        shellcode = (
                b"\x48\x31\xC0" +  # xor rax,rax
                b"\xB8\x3B\x00\x00\x02" +  # mov eax,0x200003b
                call +
                b"/usr/bin/say\x00" +
                message +
                b"\x48\x8B\x3C\x24" +  # mov rdi,[rsp]
                b"\x4C\x8D\x57\x0D" +  # lea r10,[rdi+0xd]
                b"\x48\x31\xD2" +  # xor rdx,rdx
                b"\x52" +  # push rdx
                b"\x41\x52" +  # push r10
                b"\x57" +  # push rdi
                b"\x48\x89\xE6" +  # mov rsi,rsp
                b"\x0F\x05"  # loadall286
        )

        self.output_process("Generating payload...")
        payload = self.generate(executable_format, 'x64', shellcode)

        return payload
