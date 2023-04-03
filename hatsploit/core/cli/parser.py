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

from typing import Optional, Union


class Parser(object):
    """ Subclass of hatsploit.core.cli module.

    This subclass of hatsploit.core.cli module is intended for
    providing tools for parsing.
    """

    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def parse_options(options: dict, option: Optional[str] = None) -> Union[str, list]:
        """ Parse options.

        :param dict options: options to parse, option names as keys and
        option data as items
        :param Optional[str] option: specific option to parse
        :return Union[str, list]: list of values for options or one value
        for the specific option
        """

        if not option:
            values = []

            handler_options = [
                'BLINDER', 'PAYLOAD', 'LHOST', 'LPORT', 'RBHOST', 'RBPORT', 'ENCODER',
                'RHOST', 'RPORT', 'BPORT'
            ]

            for option_name in options:
                if option_name.upper() not in handler_options:
                    values.append(str(options[option_name]['Value']))

            if len(values) == 1:
                return values[0]

            return values
        return str(options[option]['Value'])
