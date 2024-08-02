"""
This payload requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.core.payload.basic import *


class HatSploitPayload(Payload):
    def __init__(self):
        super().__init__({
            'Name': "Windows Calculator",
            'Payload': "windows/generic/calc",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - payload developer',
            ],
            'Description': "Windows calc.exe payload.",
            'Arch': ARCH_GENERIC,
            'Platform': OS_WINDOWS,
            'Type': ONE_SIDE,
        })

    def run(self):
        return "calc.exe"
