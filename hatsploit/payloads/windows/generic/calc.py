"""
This payload requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.payload.basic import *


class HatSploitPayload(Payload):
    def __init__(self):
        super().__init__()

        self.details.update({
            'Name': "Windows Calculator",
            'Payload': "windows/generic/calc",
            'Authors': [
                'Ivan Nikolsky (enty8080) - payload developer',
            ],
            'Description': "Windows calc.exe payload.",
            'Arch': ARCH_GENERIC,
            'Platform': OS_WINDOWS,
            'Rank': "high",
            'Type': "one_side",
        })

    def run(self):
        return "calc.exe"
