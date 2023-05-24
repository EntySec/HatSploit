"""
This module requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.module.basic import *


class HatSploitModule(Module):
    def __init__(self):
        super().__init__()

        self.details.update({
            'Category': "post",
            'Name': "iOS Restart SpringBoard",
            'Module': "post/apple_ios/shell/respring",
            'Authors': [
                'Ivan Nikolsky (enty8080) - module developer',
            ],
            'Description': "Restart iOS SpringBoard.app through shell.",
            'Platform': "apple_ios",
            'Rank': "medium",
        })

        self.session = SessionOption(None, "Session to run on.", True,
                                     platforms=['apple_ios'], type='shell')

    def run(self):
        self.session.session.send_command("killall SpringBoard")
