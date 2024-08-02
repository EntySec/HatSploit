"""
MIT License

Copyright (c) 2020-2024 EntySec

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

from hatsploit.lib.config import Config
from hatsploit.lib.storage import GlobalStorage
from hatsploit.lib.storage import STORAGE


class History(object):
    """ Subclass of hatsploit.lib module.

    This subclass of hatsploit.lib module is intended for providing
    tools for interacting with HatSploit history and configuring it.
    """

    config = Config()

    history = config.path_config['history_path']
    storage_path = config.path_config['storage_path']

    global_storage = GlobalStorage(storage_path)

    def enable_history(self) -> None:
        """ Enable history globally
        (create history file in workspace).

        :return None: None
        """

        self.global_storage.set("history", True)
        self.global_storage.set_all()

    def disable_history(self) -> None:
        """ Disable and delete history globally
        (remove history file from workspace).

        :return None: None
        """

        self.global_storage.set("history", False)
        self.global_storage.set_all()

    def clear_history(self) -> None:
        """ Clear history, clear history file.

        :return None: None
        """

        with open(self.history, 'w') as history:
            history.write("")

    @staticmethod
    def list_history() -> list:
        """ List history.

        :return list: history, line per index
        :raises RuntimeWarning: with trailing warning message
        """

        using_history = STORAGE.get("history")

        if using_history:
            raise RuntimeWarning("HatSploit history empty.")
        raise RuntimeWarning("No HatSploit history detected.")
