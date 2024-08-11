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

from pex.text import Text


class Exit(object):
    """ Subclass of pawn.windows.x86 module.

    This subclass of pawn.windows.x86 module is intended for
    providing code for exiting shellcode.
    """

    def __init__(self) -> None:
        super().__init__()

        self.text = Text()

    def exit_block(self, type: str) -> str:
        """ Craft exit block.

        :param str type: type of exit (see self.exit_types)
        :return str: exit block
        """

        block = dedent("""\
        exit:
        """)

        if type == 'seh':
            block += dedent(f"""\
                mov  ebx, {self.text.block_api_hash('kernel32.dll', 'SetUnhandledExceptionFilter')}
                push 0
                push ebx
                call ebp
                push 0
                ret
            """)

        elif type == 'thread':
            block += dedent(f"""\
                mov  ebx, {self.text.block_api_hash('kernel32.dll', 'ExitThread')}
                push {self.text.block_api_hash('kernel32.dll', 'GetVersion')}
                call ebp
                cmp  al, 6
                jl   quit
                cmp  bl, 0xe0
                jne  quit
                mov  ebx, {self.text.block_api_hash('ntdll.dll', 'RtlExitUserThread')}

            quit:
                push 0
                push ebx
                call ebp
            """)

        elif type == 'process':
            block += dedent(f"""\
                mov  ebx, {self.text.block_api_hash('kernel32.dll', 'ExitProcess')}
                push 0
                push ebx
                call ebp
            """)

        elif type == 'sleep':
            block += dedent(f"""\
                mov  ebx, {self.text.block_api_hash('kernel32.dll', 'Sleep')}
                push 300000
                push ebx
                call ebp
                jmp  exit
            """)

        return block
