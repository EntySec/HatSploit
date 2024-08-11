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
    """ Subclass of pawn.windows.x64 module.

    This subclass of pawn.windows.x64 module is intended for
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
            pop rax
        """)

        if type == 'seh':
            block += dedent(f"""\
                push 0
                pop  rcx
                mov  ebx, {self.text.block_api_hash('kernel32.dll', 'SetUnhandledExceptionFilter')}
                mov  r10d, ebx
                call rbp
                push 0
                ret
            """)

        elif type == 'thread':
            block += dedent(f"""\
                push 0
                pop  rcx
                mov  ebx, {self.text.block_api_hash('kernel32.dll', 'ExitThread')}
                mov  r10d, ebx
                call rbp
            """)

        elif type == 'process':
            block += dedent(f"""\
                push 0
                pop  rcx
                mov  r10, {self.text.block_api_hash('kernel32.dll', 'ExitProcess')}
                call rbp
            """)

        elif type == 'sleep':
            block += dedent(f"""\
                push 300000
                pop  rcx
                mov  r10, {self.text.block_api_hash('kernel32.dll', 'Sleep')}
                call rbp
                jmp  exit
            """)

        return block
