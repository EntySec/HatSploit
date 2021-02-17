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

from core.io import io

class badges:
    def __init__(self):
        self.io = io()

        self.BLACK = '\033[30m'
        self.RED = '\033[31m'
        self.GREEN = '\033[32m'
        self.YELLOW = '\033[33m'
        self.BLUE = '\033[34m'
        self.PURPLE = '\033[35m'
        self.CYAN = '\033[36m'
        self.WHITE = '\033[77m'

        self.END = '\033[0m'
        self.BOLD = '\033[1m'
        self.DARK = '\033[2m'
        self.BENT = '\033[3m'
        self.LINE = '\033[4m'
        self.TWINK = '\033[5m'
        self.BACK = '\033[7m'
        
        self.REMOVE = '\033[1K\r'
        self.CLEAR = '\033c'

        self.I = self.WHITE + self.BOLD + '[i] ' + self.END
        self.S = self.GREEN + self.BOLD + '[+] ' + self.END
        self.W = self.YELLOW + self.BOLD + '[!] ' + self.END
        self.E = self.RED + self.BOLD + '[-] ' + self.END
        self.P = self.BLUE + self.BOLD + '[*] ' + self.END
        self.Q = self.WHITE + self.BOLD + '[?] ' + self.END
        self.A = self.WHITE + self.BOLD + '[>] ' + self.END

    def output_empty(self, message):
        self.io.output(message)
        
    def output_usage(self, message):
        self.output_empty("Usage: " + message)
        
    def output_process(self, message):
        self.output_empty(self.P + message)

    def output_success(self, message):
        self.output_empty(self.S + message)

    def output_error(self, message):
        self.output_empty(self.E + message)

    def output_warning(self, message):
        self.output_empty(self.W + message)

    def output_information(self, message):
        self.output_empty(self.I + message)
        
    def input_empty(self, message):
        output = ""
        out = self.io.input(message)[0]
        for command in out:
            output += command + " "
        return output.strip()
        
    def input_question(self, message):
        return self.input_empty(self.Q + message)

    def input_arrow(self, message):
        return self.input_empty(self.A + message)
