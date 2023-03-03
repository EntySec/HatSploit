"""
This module requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.module import Module
from hatsploit.lib.sessions import Sessions


class HatSploitModule(Module, Sessions):
    def __init__(self):
        super().__init__()

        self.details = {
            'Category': "post",
            'Name': "iOS Restart SpringBoard",
            'Module': "post/apple_ios/shell/respring",
            'Authors': [
                'Ivan Nikolsky (enty8080) - module developer',
            ],
            'Description': "Restart iOS SpringBoard.app through shell.",
            'Platform': "apple_ios",
            'Rank': "medium",
        }

        self.options = {
            'SESSION': {
                'Description': "Session to run on.",
                'Value': None,
                'Type': {'session': {'Platforms': ['apple_ios'], 'Type': 'shell'}},
                'Required': True,
            }
        }

    def run(self):
        session = self.parse_options(self.options)
        session = self.get_session(session)

        if session:
            session.send_command("killall SpringBoard")
