#!/usr/bin/env python3

#
# This module requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.base.module import Module
from hatsploit.utils.session import SessionTools


class HatSploitModule(Module, SessionTools):
    details = {
        'Name': "macOS Shell Get PID",
        'Module': "post/macos/shell/getpid",
        'Authors': [
            'Ivan Nikolsky (enty8080)'
        ],
        'Description': "Get current session process id.",
        'Comments': [
            ''
        ],
        'Platform': "macos",
        'Risk': "medium"
    }

    options = {
        'SESSION': {
            'Description': "Session to run on.",
            'Value': 0,
            'Type': "session",
            'Required': True
        }
    }

    def run(self):
        session = self.parse_options(self.options)

        session = self.get_session('macos', 'shell', session)
        pid = session.send_command("printf $$")

        self.output_information(f"PID: {pid}")
