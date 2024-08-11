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

from .exit import Exit
from ..reflective_dll import ReflectiveDLL

from pex.assembler import Assembler


class Bootstrap(object):
    """ Subclass of pawn.windows.x86 module.

    This subclass of pawn.windows.x86 module is intended for providing
    an interface for bootstrapping DLL for the stage1.
    """

    def __init__(self) -> None:
        self.reflective_dll = ReflectiveDLL()
        self.assembler = Assembler()

        self.exit_types = Exit().exit_types

    @staticmethod
    def bootstrap_block(offset: int, exit: int) -> str:
        """ Assembly bootstrap block to inject
        to the DLL's header.

        :param int offset: offset of the DLL
        :param int exit: exit type
        :return str: bootstrap block
        """

        payload = dedent(f"""\
        start:
            dec  ebp
            pop  edx
            call 5
            pop  ebx
            push edx
            inc  ebp
            push ebp
            mov  ebp, esp
            add  ebx, {"0x%08x" % (offset - 7)}
            call ebx
            push edi
            push 4
            push eax
            mov  ebx, eax
            call ebx
            push {"0x%08x" % exit}
            push 5
            push eax
            call ebx
        """)

        return payload

    def inject_dll(self, library: str) -> bytes:
        """ Inject bootstrap to the DLL's header.

        :param str library: path to the DLL
        :return bytes: patched DLL
        """

        dll, offset = self.reflective_dll.load_rdi_dll(library)

        bootstrap = self.bootstrap_block(
            offset, self.exit_types['thread'])
        bootstrap = self.assembler.assemble('x86', bootstrap)

        if len(bootstrap) > 62:
            raise RuntimeError("Reflective DLL Injection is much bigger than e_lfanew buffer!")

        dll[:len(bootstrap)] = bootstrap
        return dll
