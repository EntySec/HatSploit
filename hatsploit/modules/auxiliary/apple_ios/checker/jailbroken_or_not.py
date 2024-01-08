"""
This module requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.module.basic import *
from pex.proto.tcp import TCPTools


class HatSploitModule(Module, TCPTools):
    def __init__(self):
        super().__init__()

        self.details.update({
            'Category': "auxiliary",
            'Name': "Jailbreak Installation Checker",
            'Module': "auxiliary/apple_ios/checker/jailbroken_or_not",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - module developer',
            ],
            'Description': "Check if remote iPhone jailbroken.",
            'Platform': OS_IPHONE,
            'Rank': "low",
        })

        self.target = IPv4Option(None, "Remote host.", True)

    def run(self):
        target = self.target.value

        self.print_process(f"Checking {target}...")
        if self.check_tcp_port(target, 22):
            self.print_success("Target device may be jailbroken!")
        else:
            self.print_warning("Looks like target device is not jailbroken.")
