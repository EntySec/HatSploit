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

        self.port.set(5555)
        self.port.visible = False
        self.host.description = "ADB host."

    def run(self):
        if self.is_on():
            self.print_success("Target device may has ADB installation!")
            return

        self.print_warning("Looks like target device has no ADB installation.")
