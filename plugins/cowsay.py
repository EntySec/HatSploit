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

import textwrap

from core.lib.plugin import HatSploitPlugin

class HatSploitPlugin(HatSploitPlugin):
    details = {
        'Name': "cowsay",
        'Authors': [
            'enty8080'
        ],
        'Description': "Cowsay plugin for HatSploit.",
        'Dependencies': [
            ''
        ],
        'Comments': [
            ''
        ]
    }

    commands = {
        'cowsay': {
            'cowsay': {
                'Description': "Ask cow to say message.",
                'Usage': "cowsay <message>",
                'MinArgs': 1
            }
        }
    }

    def ask_cow(self, message, length=40):
        return self.build_bubble(message, length) + self.build_cow()
        
    def get_border(self, lines, index):
        if len(lines) < 2:
            return ["<", ">"]
        if index == 0:
            return ["/", "\\"]
        if index == len(lines) - 1:
            return ["\\", "/"]
        return ["|", "|"]
        
    def build_cow(self):
        return """
         \   ^__^ 
          \  (oo)\_______
             (__)\       )\/\\
                 ||----w |
                 ||     ||
        """
        
    def normalize_text(self, message, length):
        lines = textwrap.wrap(message, length)
        maxlen = len(max(lines, key=len))
        return [line.ljust(maxlen) for line in lines]
    
    def build_bubble(self, message, length=40):
        bubble = []
        lines = self.normalize_text(message, length)
        bordersize = len(lines[0])
        bubble.append(" __" + "_" * bordersize)
        for index, line in enumerate(lines):
            border = self.get_border(lines, index)
            bubble.append("%s %s %s" % (border[0], line, border[1]))
        bubble.append(" --" + "-" * bordersize)
        return "\n".join(bubble)
        
    def cowsay(self, argc, argv):
        message = argv[0]
        cow = self.ask_cow(message, len(message))
        self.output_empty(cow)

    def run(self):
        message = "Cow here, moo!"
        cow = self.ask_cow(message, len(message))
        self.output_empty(cow)
        
        self.output_information("Use " + self.GREEN + "cowsay" + self.END + " to call me.")
