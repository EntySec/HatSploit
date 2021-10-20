#!/usr/bin/env python3

#
# This module requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.lib.module import Module
from hatsploit.utils.session import SessionTools


class HatSploitModule(Module, SessionTools):
    details = {
        'Name': "Windows Invoke Message Box",
        'Module': "post/windows/misc/message_box",
        'Authors': [
            'Ivan Nikolsky (enty8080) - module developer'
        ],
        'Description': "Invoke message box on Windows machine.",
        'Comments': [
            ''
        ],
        'Platform': "windows",
        'Rank': "medium"
    }

    options = {
        'SESSION': {
            'Description': "Session to run on.",
            'Value': None,
            'Type': "session->shell",
            'Required': True
        },
        'MESSAGE': {
            'Description': "Message to show.",
            'Value': "Hello, Friend!",
            'Type': None,
            'Required': True
        }
    }

    def run(self):
        session, message = self.parse_options(self.options)
        session = self.get_session(session)

        source = (
            "[reflection.assembly]::loadwithpartialname('system.windows.forms');"
            f"[system.Windows.Forms.MessageBox]::show('{message}')"
        )

        if session:
            session.send_command(f"powershell -w hidden -nop -c {source}")
