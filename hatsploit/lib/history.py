"""
MIT License

Copyright (c) 2020-2022 EntySec

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import readline

from hatsploit.lib.config import Config
from hatsploit.lib.storage import GlobalStorage
from hatsploit.lib.storage import LocalStorage


class History(object):
    def __init__(self):
        super().__init__()

        self.config = Config()
        self.local_storage = LocalStorage()

        self.history = self.config.path_config['history_path']
        self.storage_path = self.config.path_config['storage_path']

        self.global_storage = GlobalStorage(self.storage_path)

    def enable_history(self):
        self.global_storage.set("history", True)
        self.global_storage.set_all()

    def disable_history(self):
        self.global_storage.set("history", False)
        self.global_storage.set_all()

        readline.clear_history()
        with open(self.history, 'w') as history:
            history.write("")

    def clear_history(self):
        readline.clear_history()

        with open(self.history, 'w') as history:
            history.write("")

    def list_history(self):
        using_history = self.local_storage.get("history")

        if using_history:
            if readline.get_current_history_length() > -1:
                history = []

                for index in range(1, readline.get_current_history_length() + 1):
                    history.append(readline.get_history_item(index))
                return history

            raise RuntimeWarning("HatSploit history empty.")
        raise RuntimeWarning("No HatSploit history detected.")
