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
        'Name': "Unix Shell Get PID",
        'Module': "post/unix/shell/getpid",
        'Authors': [
            'Ivan Nikolsky (enty8080) - module developer'
        ],
        'Description': "Get current session process id.",
        'Platform': "unix",
        'Rank': "medium"
    }

    options = {
        'SESSION': {
            'Description': "Session to run on.",
            'Value': None,
            'Type': "session->[unix,linux,macos]",
            'Required': True
        }
    }

    def run(self):
        session = self.parse_options(self.options)
        session = self.get_session(session)

        if session:
            pid = session.send_command("printf $$", True).strip()
            if pid:
                self.print_information(f"PID: {pid}")
