"""
MIT License

Copyright (c) 2020-2023 EntySec

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
import sys

from colorscript import ColorScript

from hatsploit.core.cli.colors import Colors
from hatsploit.core.cli.fmt import FMT
from hatsploit.lib.storage import LocalStorage

patch = False

try:
    import gnureadline as readline

except Exception:
    import readline
    patch = True


class IO(object):
    """ Subclass of hatsploit.core.base module.

    This subclass of hatsploit.core.base module is intended for
    providing an implementation of I/O for HatSploit interpreter.
    """

    def __init__(self) -> None:
        super().__init__()

        self.local_storage = LocalStorage()
        self.fmt = FMT()
        self.color_script = ColorScript()

    def print(self, message: str = '', start: str = '%remove', end: str = '%newline') -> None:
        """ Print string.

        :param str message: message to print
        :param str start: string to print before the message
        :param str end: string to print after the message
        :return None: None
        """

        line = self.color_script.parse(start + message + end)
        use_log = self.local_storage.get("log")

        sys.stdout.write(line)
        sys.stdout.flush()

        if use_log:
            with open(use_log, 'a') as f:
                f.write(line)
                f.flush()

        if self.local_storage.get("prompt"):
            prompt = self.local_storage.get("prompt") + readline.get_line_buffer()
            sys.stdout.write(prompt)
            sys.stdout.flush()

    def input(self, message: str = '', start: str = '%remove%end', end: str = '%end') -> list:
        """ Input string.

        :param str message: message to print
        :param str start: string to print before the message
        :param str end: string to print after the message
        :return list: read string separated by space and commas
        """

        message = start + message + end

        if patch:
            message = self.color_script.libreadline(message)

        line = self.color_script.parse(message)

        use_log = self.local_storage.get("log")
        self.local_storage.set("prompt", line)

        if use_log:
            with open(use_log, 'a') as f:
                f.write(line)
                f.flush()

        commands = input(line)

        if use_log:
            with open(use_log, 'a') as f:
                f.write(commands + '\n')
                f.flush()

        commands = self.fmt.format_commands(commands)

        self.local_storage.set("prompt", None)
        return commands
