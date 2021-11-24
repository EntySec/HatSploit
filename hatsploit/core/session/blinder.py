#!/usr/bin/env python3

#
# MIT License
#
# Copyright (c) 2020-2021 EntySec
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

from hatsploit.core.cli.badges import Badges


class Blinder:
    badges = Badges()

    def blinder(self, sender, args=[]):
        self.badges.print_empty()
        self.badges.print_information("Welcome to Blinder, blind command injection handler.")
        self.badges.print_information("Blinder is not a reverse shell, just a blind command injection.")
        self.badges.print_empty()

        while True:
            commands = self.badges.input_empty("%lineblinder%end > ")
            command = ' '.join(commands)

            if not command.strip() or command == 'exit':
                return

            self.badges.print_process("Sending command to target...")
            output = sender(*args, command)
            if output:
                self.badges.print_empty(f'\n{output}')
            self.badges.print_empty('')
