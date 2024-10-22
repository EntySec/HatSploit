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

from hatsploit.lib.core.payload.basic import (
    ARCH_X64,
    ARCH_X86
)

from hatsploit.lib.ui.option import (
    BooleanOption
)


class MacOS(BaseMixin):
    """ Main class of hatsploit.lib.core.payload.macos module.

    This main class of hatsploit.lib.core.payload module is intended
    to provide macOS-specific payload options.
    """

    def __init__(self, info: dict = {}) -> None:
        """ Initialize macOS mixin.

        :param dict info: mixin info
        :return None: None
        """

        super().__init__(info)

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

        return payload

    def apply_x64(self, payload: bytes) -> bytes:
        """ Prepend/append available x64 prepends/appends.

        :param bytes payload: payload data
        :return bytes: payload
        """

        prepend = b""
        append = b""

        if self.setreuid.value:
            prepend += self.__asm__(
                """
                setreuid:
                    mov r8b, 0x2
                    shl r8, 24
                    or r8, 126
                    mov rax, r8
                    xor rdi, rdi
                    xor rsi, rsi
                    syscall
                """
            )

        if self.setuid.value:
            prepend += self.__asm__(
                """
                setuid:
                    mov r8b, 0x2
                    shl r8, 24
                    or r8, 23
                    mov rax, r8
                    xor rdi, rdi
                    syscall
                """
            )

        if self.setregid.value:
            prepend += self.__asm__(
                """
                setregid:
                    mov r8b, 0x2
                    shl r8, 24
                    or r8, 127
                    mov rax, r8
                    xor rdi, rdi
                    xor rsi, rsi
                    syscall
                """
            )

        if self.setgid.value:
            prepend += self.__asm__(
                """
                setgid:
                    mov r8b, 0x2
                    shl r8, 23
                    or r8, 90
                    shl r8, 1
                    or r8, 1
                    mov rax, r8
                    xor rdi, rdi
                    syscall
                """
            )

        if self.exit.value:
            append += self.__asm__(
                """
                exit:
                    mov r8b, 0x2
                    shl r8, 24
                    or r8, 1
                    mov rax, r8
                    xor rdi, rdi
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

        if self.setreuid.value:
            prepend += self.__asm__(
                """
                setreuid:
                    xor eax, eax
                    push eax
                    push eax
                    push eax
                    mov al, 0x7e
                    int 0x80
                """
            )

        if self.setuid.value:
            prepend += self.__asm__(
                """
                setuid:
                    xor eax, eax
                    push eax
                    push eax
                    mov al, 0x17
                    int 0x80
                """
            )

        if self.setregid.value:
            prepend += self.__asm__(
                """
                setregid:
                    xor eax, eax
                    push eax
                    push eax
                    push eax
                    mov al, 0x7f
                    int 0x80
                """
            )

        if self.setgid.value:
            prepend += self.__asm__(
                """
                setgid:
                    xor eax, eax
                    push eax
                    push eax
                    mov al, 0xb5
                    int 0x80
                """
            )

        if self.exit.value:
            append += self.__asm__(
                """
                exit:
                    xor eax, eax
                    push eax
                    movb al, 0x01
                    int 0x80
                """
            )

        return prepend + payload + append
