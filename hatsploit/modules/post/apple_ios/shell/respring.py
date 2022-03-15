#!/usr/bin/env python3

#
# This module requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.lib.module import Module
from hatsploit.lib.sessions import Sessions


class HatSploitModule(Module, Sessions):
    details = {
        'Category': "post",
        'Name': "iOS Restart SpringBoard",
        'Module': "post/apple_ios/shell/respring",
        'Authors': [
            'Ivan Nikolsky (enty8080) - module developer'
        ],
        'Description': "Restart iOS SpringBoard.app through shell.",
        'Platform': "apple_ios",
        'Rank': "medium"
    }

    options = {
        'SESSION': {
            'Description': "Session to run on.",
            'Value': None,
            'Type': "session",
            'Required': True
        }
    }

    def run(self):
        session = self.parse_options(self.options)
        session = self.get_session(session)

        if session:
            session.send_command("killall SpringBoard")
