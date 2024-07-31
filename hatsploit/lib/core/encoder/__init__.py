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

from typing import Optional

from hatsploit.lib.ui.option import IntegerOption
from hatsploit.lib.ui.options import Options

from hatsploit.lib.base import BaseMixin


class Encoder(BaseMixin, Options):
    """ Subclass of hatsploit.lib module.

    This subclass of hatsploit.lib module is intended for providing
    wrapper for a encoder.
    """

    def __init__(self, info: dict = {}) -> None:
        """ Initialize encoder

        :param dict info: encoder details
        :return None: None
        """

        details = {
            'Name': "",
            'Encoder': "",
            'Authors': (
            ),
            'Description': "",
            'Arch': None,
        }
        details.update(info)

        super().__init__(details)

        self.options = {}
        self.advanced = {}
        self.iterations = IntegerOption('ITER', 1, "Number of iterations.", False, True)

    def __call__(self) -> None:
        """ Called after initialization.

        :return None: None
        """

        return

    def run(self) -> None:
        """ Run this encoder.

        :return None: None
        """

        return
