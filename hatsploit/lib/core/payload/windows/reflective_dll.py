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

import pefile

from typing import Tuple, Any


class ReflectiveDLL(object):
    """ Subclass of pawn.windows module.

    This subclass of pawn.windows module is intended for providing
    a representation of Reflective DLL Loader for Windows.
    """

    def load_rdi_dll(self, path: str, name: str = 'ReflectiveLoader', ordinal: int = 1) -> Tuple[bytes, Any]:
        """ Load a reflectively-injectable DLL from disk and find the offset
        to the ReflectiveLoader function inside the DLL.

        :param str path: path to the DLL to load
        :param str name: reflective loader function name
        :param int ordinal: ordinal of the reflective loader
        :return Tuple[bytes, Any]: DLL data and offset
        """

        with open(path, 'rb') as f:
            dll = f.read()
            offset = self.parse_pe(dll, name, ordinal)

            if not offset:
                raise RuntimeError("Cannot find the ReflectiveLoader entry point!")

        return dll, offset

    def load_rdi_dll_from_data(self, dll: bytes, name: str = 'ReflectiveLoader', ordinal: int = 1) -> Tuple[bytes, Any]:
        """ Load a reflectively-injectable DLL from disk and find the offset
        to the ReflectiveLoader function inside the DLL.

        :param bytes dll: DLL data
        :param str name: reflective loader function name
        :param int ordinal: ordinal of the reflective loader
        :return Tuple[bytes, Any]: DLL data and offset
        """

        offset = self.parse_pe(dll, name, ordinal)

        if not offset:
            raise RuntimeError("Cannot find the ReflectiveLoader entry point!")

        return dll, offset

    @staticmethod
    def parse_pe(dll: bytes, name: str = 'ReflectiveLoader', ordinal: int = 0x1) -> Tuple[bytes, int]:
        """ Parse PE and find an offset of reflective loader.

        :param bytes dll: DLL data
        :param str name: reflective loader function name
        :param int ordinal: ordinal of the reflective loader
        :return Tuple[bytes, int]: DLL data and offset
        """

        pe = pefile.PE(data=dll)
        offset = None

        if name:
            for exp in pe.DIRECTORY_ENTRY_EXPORT.symbols:
                if loader_name.encode() in exp.name:
                    offset = exp.address
                    break

        if offset is not None and ordinal:
            for exp in pe.DIRECTORY_ENTRY_EXPORT.symbols:
                if exp.ordinal == ordinal:
                    offset = exp.address
                    break

        return offset
