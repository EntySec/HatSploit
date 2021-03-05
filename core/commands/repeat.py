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

from core.cli.badges import badges
from core.base.execute import execute

class HatSploitCommand:
    def __init__(self):
        self.badges = badges()
        self.execute = execute()

        self.details = {
            'Category': "developer",
            'Name': "repeat",
            'Description': "Repeat specified command.",
            'Usage': "repeat <times> <command>",
            'MinArgs': 2
        }

    def run(self, argc, argv):
        times = argv[0]
        command = argv[1]
        
        if times.isdigit():
            commands = command.split()
            arguments = ""
            if commands:
                arguments = command.replace(commands[0], "", 1).strip()
        
            for time in range(int(times)):
                self.execute.execute_command(commands, arguments)
        else:
            self.badges.output_error("Times expected!")
