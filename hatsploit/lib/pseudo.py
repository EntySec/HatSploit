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

from typing import Callable, Any
from badges import Badges


class Pseudo(Badges):
    """ Subclass of hatsploit.lib module.

    This subclass of hatsploit.lib module is intended for providing
    an implementation of Pseudo Shell, OS command injection handler.
    """

    def shell(self, sender: Callable[..., Any]) -> None:
        """ Blinder shell, aka command handler.

        :param Callable sender: function via which Blinder sends commands
        :return None: None
        """

        self.print_empty()
        self.print_information("Welcome to Pseudo Shell, OS command injection handler.")
        self.print_information("Pseudo shell is not a reverse shell, just a straight command injection.")
        self.print_empty()

        while True:
            command = self.input_empty("%linepseudo%end % ")

            if not command.strip() or command == 'exit':
                return

            self.print_process("Sending command to target...")
            output = sender(command)

            if output:
                self.print_empty(f'\n{output}')

            self.print_empty()
