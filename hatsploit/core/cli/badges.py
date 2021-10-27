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

import os

from hatsploit.core.base.io import IO
from hatsploit.core.utils.ui.colors_script import ColorsScript


class Badges:
    io = IO()
    colors_script = ColorsScript()

    def print_empty(self, message="", start='\033[1K\r', end='\n'):
        line = self.colors_script.parse(message)
        self.io.print(line, start=start, end=end)

    def print_usage(self, message, start='\033[1K\r', end='\n'):
        self.print_empty(f"Usage: {message}", start=start, end=end)

    def print_process(self, message, start='\033[1K\r', end='\n'):
        self.print_empty(f"%bold%blue[*]%end {message}", start=start, end=end)

    def print_success(self, message, start='\033[1K\r', end='\n'):
        self.print_empty(f"%bold%green[+]%end {message}", start=start, end=end)

    def print_error(self, message, start='\033[1K\r', end='\n'):
        self.print_empty(f"%bold%red[-]%end {message}", start=start, end=end)

    def print_warning(self, message, start='\033[1K\r', end='\n'):
        self.print_empty(f"%bold%yellow[!]%end {message}", start=start, end=end)

    def print_information(self, message, start='\033[1K\r', end='\n'):
        self.print_empty(f"%bold%white[i]%end {message}", start=start, end=end)

    def print_multi(self, message):
        self.print_empty(f"%bold%blue[*]%end {message}", start='\r', end='')

    def input_empty(self, message):
        line = self.colors_script.parse(message)

        output = ""
        out = self.io.input(line)[0]

        for command in out:
            output += command + " "
        return output.strip()

    def input_question(self, message):
        return self.input_empty(f"%bold%white[?]%end {message}")

    def input_arrow(self, message):
        return self.input_empty(f"%bold%white[>]%end {message}")
