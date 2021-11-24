#!/usr/bin/env python3

#
# This module requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.lib.module import Module
from hatsploit.utils.session import SessionTools


class HatSploitModule(Module, SessionTools):
    details = {
        'Name': "macOS Shell Suspend",
        'Module': "post/macos/shell/suspend",
        'Authors': [
            'Ivan Nikolsky (enty8080) - module developer'
        ],
        'Description': "Suspend macOS through shell.",
        'Comments': [
            ''
        ],
        'Platform': "macos",
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
            session.send_command(
                "/System/Library/CoreServices/Menu\ Extras/User.menu/Contents/Resources/CGSession -suspend")
