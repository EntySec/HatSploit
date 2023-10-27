"""
This payload requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.payload.basic import *
from pex.socket import Socket


class HatSploitPayload(Payload, Handler, Socket):
    def __init__(self):
        super().__init__()

        self.details.update({
            'Name': "Windows x86 Shell Reverse TCP",
            'Payload': "windows/x86/shell_reverse_tcp",
            'Authors': [
                'Ivan Nikolsky (enty8080) - payload developer',
            ],
            'Description': "Reverse shell TCP payload for Windows x86.",
            'Arch': ARCH_X64,
            'Platform': OS_WINDOWS,
            'Rank': "low",
            'Type': "reverse_tcp",
        })

    def run(self):
        return b""
