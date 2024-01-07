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

from hatsploit.core.base.io import IO


class Badges(object):
    """ Subclass of hatsploit.core.cli module.

    This subclass of hatsploit.core.cli module is intended for
    providing various printing interfaces.
    """

    def __init__(self) -> None:
        super().__init__()

        self.io = IO()

    def print_empty(self, message: str = '', start: str = '%remove', end: str = '%newline') -> None:
        """ Print string with empty start.

        :param str message: message to print
        :param str start: string to print before the message
        :param str end: string to print after the message
        :return None: None
        """

        self.io.print(message, start, end)

    def print_usage(self, message: str, start: str = '%remove', end: str = '%newline') -> None:
        """ Print string with Usage: start.

        :param str message: message to print
        :param str start: string to print before the message
        :param str end: string to print after the message
        :return None: None
        """

        self.print_empty(f"Usage: {message}", start, end)

    def print_process(self, message: str, start: str = '%remove', end: str = '%newline') -> None:
        """ Print string with [*] start.

        :param str message: message to print
        :param str start: string to print before the message
        :param str end: string to print after the message
        :return None: None
        """

        self.print_empty(f"%bold%blue[*]%end {message}", start, end)

    def print_success(self, message: str, start: str = '%remove', end: str = '%newline') -> None:
        """ Print string with [+] start.

        :param str message: message to print
        :param str start: string to print before the message
        :param str end: string to print after the message
        :return None: None
        """

        self.print_empty(f"%bold%green[+]%end {message}", start, end)

    def print_error(self, message: str, start: str = '%remove', end: str = '%newline') -> None:
        """ Print string with [-] start.

        :param str message: message to print
        :param str start: string to print before the message
        :param str end: string to print after the message
        :return None: None
        """

        self.print_empty(f"%bold%red[-]%end {message}", start, end)

    def print_warning(self, message: str, start: str = '%remove', end: str = '%newline') -> None:
        """ Print string with [!] start.

        :param str message: message to print
        :param str start: string to print before the message
        :param str end: string to print after the message
        :return None: None
        """

        self.print_empty(f"%bold%yellow[!]%end {message}", start, end)

    def print_information(self, message: str, start: str = '%remove', end: str = '%newline') -> None:
        """ Print string with [i] start.

        :param str message: message to print
        :param str start: string to print before the message
        :param str end: string to print after the message
        :return None: None
        """

        self.print_empty(f"%bold%white[i]%end {message}", start, end)

    def input_empty(self, message: str = '', start: str = '%remove%end', end: str = '%end') -> str:
        """ Input string with empty start.

        :param str message: message to print
        :param str start: string to print before the message
        :param str end: string to print after the message
        :return str: read string
        """

        return self.io.input(message, start, end)

    def input_question(self, message: str, start: str = '%remove%end', end: str = '%end') -> str:
        """ Input string with [?] start.

        :param str message: message to print
        :param str start: string to print before the message
        :param str end: string to print after the message
        :return str: read string
        """

        return self.input_empty(f"%bold%white[?]%end {message}", start, end)

    def input_arrow(self, message: str, start: str = '%remove%end', end: str = '%end') -> str:
        """ Input string with [>] start.

        :param str message: message to print
        :param str start: string to print before the message
        :param str end: string to print after the message
        :return str: read string
        """

        return self.input_empty(f"%bold%white[>]%end {message}", start, end)
