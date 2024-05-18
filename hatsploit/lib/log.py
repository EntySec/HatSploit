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

import os

from hatsploit.lib.config import Config
from hatsploit.lib.storage import GlobalStorage


class Log(object):
    """ Subclass of hatsploit.lib module.

    This subclass of hatsploit.lib module is intended for providing
    tools for interacting with HatSploit logs and configuring them.
    """

    def __init__(self) -> None:
        super().__init__()

        self.config = Config()

        self.storage_path = self.config.path_config['storage_path']
        self.global_storage = GlobalStorage(self.storage_path)

    def enable_log(self, filename: str) -> None:
        """ Enable logging globally
        (create log file in workspace).

        :param str filename: log file name
        :return None: None
        """

        self.global_storage.set("log", filename)
        self.global_storage.set_all()

    def disable_log(self) -> None:
        """ Disable logging globally.

        :return None: None
        """

        self.global_storage.set("log", None)
        self.global_storage.set_all()
