#!/usr/bin/env python3

#
# This module requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.lib.module import Module
from hatsploit.utils.session import SessionTools


class HatSploitModule(Module, SessionTools):
    details = {
        'Name': "Unix Shell Get PID",
        'Module': "post/unix/shell/getpid",
        'Authors': [
            'Ivan Nikolsky (enty8080) - module developer'
        ],
        'Description': "Get current session process id.",
        'Comments': [
            ''
        ],
        'Platform': "unix",
        'Risk': "medium"
    }

    options = {
        'SESSION': {
            'Description': "Session to run on.",
            'Value': 0,
            'Type': "session->[unix,linux,macos]",
            'Required': True
        }
    }

    def run(self):
        session = self.parse_options(self.options)

        session = self.get_session(session)
        pid = session.send_command("printf $$", output=True)

        self.output_information(f"PID: {pid}")
