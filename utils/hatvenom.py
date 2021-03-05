#!/usr/bin/env python3

#
# MIT License
#
# Copyright (c) 2020-2021 EntySec
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import struct

from core.base.config import config

class hatvenom:
    def __init__(self):
        self.config = config()

        self.formats = {
            'elf': self.generate_elf,
            'macho': self.generate_macho,
            'c': self.generate_c
        }
        
        self.macho_templates = {
            'x64': self.config.path_config['base_paths']['data_path'] + "utils/hatvenom/templates/macho_x64.bin",
            'aarch64': self.config.path_config['base_paths']['data_path'] + "utils/hatvenom/templates/macho_aarch64.bin"
        }
        
        self.elf_headers = {
            'armle': (
                b"\x7f\x45\x4c\x46\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                b"\x02\x00\x28\x00\x01\x00\x00\x00\x54\x80\x00\x00\x34\x00\x00\x00"
                b"\x00\x00\x00\x00\x00\x00\x00\x00\x34\x00\x20\x00\x01\x00\x00\x00"
                b"\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x80\x00\x00"
                b"\x00\x80\x00\x00\xef\xbe\xad\xde\xef\xbe\xad\xde\x07\x00\x00\x00"
                b"\x00\x10\x00\x00"
            ),
            'mipsbe': (
                b"\x7f\x45\x4c\x46\x01\x02\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                b"\x00\x02\x00\x08\x00\x00\x00\x01\x00\x40\x00\x54\x00\x00\x00\x34"
                b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x34\x00\x20\x00\x01\x00\x00"
                b"\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x40\x00\x00"
                b"\x00\x40\x00\x00\xde\xad\xbe\xef\xde\xad\xbe\xef\x00\x00\x00\x07"
                b"\x00\x00\x10\x00"
            ),
            'mipsle': (
                b"\x7f\x45\x4c\x46\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                b"\x02\x00\x08\x00\x01\x00\x00\x00\x54\x00\x40\x00\x34\x00\x00\x00"
                b"\x00\x00\x00\x00\x00\x00\x00\x00\x34\x00\x20\x00\x01\x00\x00\x00"
                b"\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x40\x00"
                b"\x00\x00\x40\x00\xef\xbe\xad\xde\xef\xbe\xad\xde\x07\x00\x00\x00"
                b"\x00\x10\x00\x00"
            ),
            'x86': (
                b"\x7f\x45\x4c\x46\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                b"\x02\x00\x03\x00\x01\x00\x00\x00\x54\x80\x04\x08\x34\x00\x00\x00"
                b"\x00\x00\x00\x00\x00\x00\x00\x00\x34\x00\x20\x00\x01\x00\x00\x00"
                b"\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x80\x04\x08"
                b"\x00\x80\x04\x08\xef\xbe\xad\xde\xef\xbe\xad\xde\x07\x00\x00\x00"
                b"\x00\x10\x00\x00"
            ),
            'aarch64': (
                b"\x7f\x45\x4c\x46\x02\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                b"\x02\x00\xb7\x00\x00\x00\x00\x00\x78\x00\x00\x00\x00\x00\x00\x00"
                b"\x40\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                b"\x00\x00\x00\x00\x40\x00\x38\x00\x01\x00\x00\x00\x00\x00\x00\x00"
                b"\x01\x00\x00\x00\x07\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                b"\xef\xbe\xad\xde\x00\x00\x00\x00\xef\xbe\xad\xde\x00\x00\x00\x00"
                b"\x00\x10\x00\x00\x00\x00\x00\x00"
            ),
            'x64': (
                b"\x7f\x45\x4c\x46\x02\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                b"\x02\x00\x3e\x00\x01\x00\x00\x00\x78\x00\x40\x00\x00\x00\x00\x00"
                b"\x40\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                b"\x00\x00\x00\x00\x40\x00\x38\x00\x01\x00\x00\x00\x00\x00\x00\x00"
                b"\x01\x00\x00\x00\x07\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                b"\x00\x00\x40\x00\x00\x00\x00\x00\x00\x00\x40\x00\x00\x00\x00\x00"
                b"\x41\x41\x41\x41\x41\x41\x41\x41\x42\x42\x42\x42\x42\x42\x42\x42"
                b"\x00\x10\x00\x00\x00\x00\x00\x00"
            )
        }

    #
    # Functions to convert data to bytes
    #
        
    def host_to_bytes(self, host):
        result = b""
        for i in host.split("."):
            result += bytes([int(i)])
        return result
        
    def port_to_bytes(self, port):
        result = "%.4x" % int(port)
        return bytes.fromhex(result)

    #
    # Functions to generate
    #
    
    def generate(self, file_format, arch, data):
        if file_format in self.formats.keys():
            return self.formats[file_format](arch, data)
        return None

    def generate_elf(self, arch, data):
        if arch in self.elf_headers.keys():
            elf = self.elf_headers[arch] + data

            if elf[4] == 1:
                if arch.endswith("be"):
                    p_filesz = struct.pack(">L", len(elf))
                    p_memsz = struct.pack(">L", len(elf) + len(data))
                else:
                    p_filesz = struct.pack("<L", len(elf))
                    p_memsz = struct.pack("<L", len(elf) + len(data))
                content = elf[:0x44] + p_filesz + p_memsz + elf[0x4c:]
            elif elf[4] == 2:
                if arch.endswith("be"):
                    p_filesz = struct.pack(">Q", len(elf))
                    p_memsz = struct.pack(">Q", len(elf) + len(data))
                else:
                    p_filesz = struct.pack("<Q", len(elf))
                    p_memsz = struct.pack("<Q", len(elf) + len(data))

                content = elf[:0x60] + p_filesz + p_memsz + elf[0x70:]
            return content
        return None
    
    def generate_macho(self, arch, data):
        if arch in self.macho_templates.keys():
            if os.path.exists(self.macho_templates[arch]):
                macho_file = open(self.macho_templates[arch], 'rb')
                macho = macho_file.read()
                macho_file.close()

                payload_index = macho.index(b'PAYLOAD:')
                data = macho[:payload_index] + data + macho[payload_index + len(data):]

                return content
        return None

    def generate_c(self, arch, data):
        shellcode = "unsigned char shellcode[] = {\n    \""
        for idx, x in enumerate(data):
            if idx % 15 == 0 and idx != 0:
                shellcode += "\"\n    \""
            shellcode += "\\x%02x" % x
        shellcode += "\"\n};\n"
        
        c = ""
        c += "#include <stdio.h>\n"
        c += "#include <string.h>\n"
        c += "\n"
        c += shellcode
        c += "\n"
        c += "int main()\n"
        c += "{\n"
        c += "    int (*ret)() = (int(*)())shellcode;\n"
        c += "    ret();\n"
        c += "}\n"
        
        return c.encode()
