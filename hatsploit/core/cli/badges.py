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


class Badges:
    io = IO()

    def print_empty(self, message='', start='%remove', end='%newline'):
        self.io.print(message, start, end)

    def print_usage(self, message, start='%remove', end='%newline'):
        self.print_empty(f"Usage: {message}", start, end)

    def print_process(self, message, start='%remove', end='%newline'):
        self.print_empty(f"%bold%blue[*]%end {message}", start, end)

    def print_success(self, message, start='%remove', end='%newline'):
        self.print_empty(f"%bold%green[+]%end {message}", start, end)

    def print_error(self, message, start='%remove', end='%newline'):
        self.print_empty(f"%bold%red[-]%end {message}", start, end)

    def print_warning(self, message, start='%remove', end='%newline'):
        self.print_empty(f"%bold%yellow[!]%end {message}", start, end)

    def print_information(self, message, start='%remove', end='%newline'):
        self.print_empty(f"%bold%white[i]%end {message}", start, end)

    def input_empty(self, message='', start='%remove%end', end='%end'):
        return self.io.input(message, start, end)

    def input_question(self, message, start='%remove%end', end='%end'):
        return self.input_empty(f"%bold%white[?]%end {message}", start, end)

    def input_arrow(self, message, start='%remove%end', end='%end'):
        return self.input_empty(f"%bold%white[>]%end {message}", start, end)
