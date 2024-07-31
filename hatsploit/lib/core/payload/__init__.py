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
from hatasm import HatAsm

from hatsploit.lib.ui.option import BytesOption
from hatsploit.lib.ui.options import Options

from hatsploit.lib.base import BaseMixin


class Payload(BaseMixin, Options):
    """ Subclass of hatsploit.lib module.

    This subclass of hatsploit.lib module is intended for providing
    wrapper for a payload.
    """

    def __init__(self, info: dict = {}) -> None:
        """ Initialize payload

        :param dict info: payload details
        :return None: None
        """

        details = {
            'Category': "single",
            'Name': "",
            'Payload': "",
            'Authors': (
            ),
            'Description': "",
            'Arch': None,
            'Platform': None,
            'Phased': False,
            'Phase': '',
            'Type': None,
            'Conversion': {
            },
        }
        details.update(info)

        super().__init__(details)

        self.options = {}
        self.advanced = {}

        self.phased = BooleanOption(
            'Phased',
            'no',
            "Send phase instead of whole payload.",
            False,
            advanced=True
        )
        self.badchars = BytesOption(
            'BadChars',
            '',
            "Bad characters to omit.",
            False,
            advanced=True
        )

    def __call__(self) -> None:
        """ Called after initialization.

        :return None: None
        """

        return

    def run(self) -> None:
        """ Run this payload.

        :return None: None
        """

        return

    def assemble(self, code: str, *args, **kwargs) -> bytes:
        """ Assemble assembly code using current architecture.

        :param str code: assembly code
        :return bytes: assembled code
        """

        return HatAsm().assemble(self.info['Arch'], code, *args, **kwargs)
