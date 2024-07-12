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
            'Name': "ADB Installation Checker",
            'Module': "auxiliary/android/checker/check_adb_installation",
            'Authors': [
                "Ivan Nikolskiy (enty8080) - module developer",
            ],
            'Description': (
                "Check if remote Android device has ADB installation."
            ),
            'Platform': OS_ANDROID,
            'Rank': LOW_RANK,
        })

        self.target = IPv4Option(None, "Remote host.", True)

    def run(self):
        target = self.target.value

        self.print_process(f"Checking {target}...")

        if self.check_tcp_port(target, 5555):
            self.print_success("Target device may has ADB installation!")
        else:
            self.print_warning("Looks like target device has no ADB installation.")
