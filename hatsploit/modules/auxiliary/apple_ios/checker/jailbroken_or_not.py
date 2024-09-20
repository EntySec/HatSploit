"""
This module requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.core.module.basic import *
from hatsploit.lib.core.module.proto import TCP


class HatSploitModule(Module, TCP):
    def __init__(self):
        super().__init__({
            'Category': "auxiliary",
            'Name': "Jailbreak Installation Checker",
            'Module': "auxiliary/apple_ios/checker/jailbroken_or_not",
            'Authors': [
                "Ivan Nikolskiy (enty8080) - module developer",
            ],
            'Description': "Check if remote iPhone jailbroken.",
            'Platform': OS_IPHONE,
            'Rank': LOW_RANK,
        })

    def __call__(self):
        self.port.set(22)
        self.port.visible = False
        self.host.description = "iPhone host."

    def run(self):
        if self.is_on():
            self.print_success("Target device may be jailbroken!")
            return

        self.print_warning("Looks like target device is not jailbroken.")
