"""
This payload requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.payload.basic import *


class HatSploitPayload(Payload):
    def __init__(self):
        super().__init__()

        self.details.update({
            'Name': "Unix Custom Command",
            'Payload': "unix/generic/custom",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - payload developer',
            ],
            'Description': "Send custom command.",
            'Arch': ARCH_GENERIC,
            'Platform': OS_UNIX,
            'Type': OneSide,
        })

        self.command = Option(None, 'Command to send', True)

    def run(self):
        return self.command
