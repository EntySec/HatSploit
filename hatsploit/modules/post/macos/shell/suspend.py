"""
This module requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.module.basic import *


class HatSploitModule(Module):
    def __init__(self):
        super().__init__()

        self.details = {
            'Category': "post",
            'Name': "macOS Shell Suspend",
            'Module': "post/macos/shell/suspend",
            'Authors': [
                'Ivan Nikolsky (enty8080) - module developer',
            ],
            'Description': "Suspend macOS through shell.",
            'Platform': "macos",
            'Rank': "medium",
        }

        self.session = SessionOption(None, "Session to run on.", True,
                                     platforms=['macos'], type='shell')

    def run(self):
        self.session.session.send_command(
            "/System/Library/CoreServices/Menu\ Extras/User.menu/Contents/Resources/CGSession -suspend"
        )
