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

from typing import Union
from pawn import Pawn

from hatsploit.lib.option import *

from hatsploit.core.cli.badges import Badges
from hatsploit.core.cli.tables import Tables
from hatsploit.core.cli.tools import Tools


class Payload(Badges, Tables, Tools, Pawn):
    """ Subclass of hatsploit.lib module.

    This subclass of hatsploit.lib module is intended for providing
    wrapper for a payload.
    """

    def __init__(self) -> None:
        super().__init__()

        self.details = {
            'Name': "",
            'Payload': "",
            'Authors': [
                ''
            ],
            'Description': "",
            'Arch': None,
            'Platform': None,
            'Session': None,
            'Rank': "",
            'Type': ""
        }

        self.badchars = BytesOption(None, "Bad characters to omit.", False, True)

    def phase(self) -> Union[bytes, None]:
        """ First phase.

        :return bytes: bytes
        """

        type = self.details['Type']

        if type not in ['reverse_tcp', 'bind_tcp']:
            type = 'reverse_tcp'

        phase = self.auto_pawn(
            platform=self.details['Platform'],
            arch=self.details['Arch'],
            type=type
        )

        if phase:
            if type == 'reverse_tcp':
                phase.set('host', self.rhost.value)
                phase.set('port', self.rport.value)

            elif type == 'bind_tcp':
                phase.set('port', self.rport.value)

            return self.run_pawn(phase)

    def run(self) -> None:
        """ Run this payload.

        :return None: None
        """

        pass
