"""
This module requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.core.module.basic import *


class HatSploitModule(Module):
    def __init__(self):
        super().__init__({
            'Category': "post",
            'Name': "iOS Restart SpringBoard",
            'Module': "post/apple_ios/shell/respring",
            'Authors': [
                "Ivan Nikolskiy (enty8080) - module developer",
            ],
            'Description': (
                "Restart iOS SpringBoard.app through shell."
            ),
            'Platform': OS_IPHONE,
            'Rank': MEDIUM_RANK,
        })

        self.session = SessionOption('SESSION', None, "Session to run on.", True,
                                     platforms=[OS_IPHONE], type='shell')

    def run(self):
        self.session.session.send_command("killall SpringBoard")
