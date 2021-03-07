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

from core.cli.fmt import fmt
from core.cli.badges import badges
from core.cli.colors import colors
from core.cli.parser import parser
from core.cli.tables import tables

class HatSploitModule:
    def __init__(self):
        self.fmt = fmt()
        self.badges = badges()
        self.colors = colors()
        self.parser = parser()
        self.tables = tables()

        self.details = {
            'Name': "",
            'Module': "",
            'Authors': [
                ''
            ],
            'Description': "",
            'Dependencies': [
                ''
            ],
            'Comments': [
                ''
            ],
            'Risk': ""
        }
        
        self.options = {
            '': {
                'Description': "",
                'Value': None,
                'Required': True
            }
        }

        self.commands = {
            '': {
                'Description': "",
                'Usage': "",
                'MinArgs': 0,
                'Run': self.command
            }
        }

    def command(self, argc, argv):
        pass
        
    def run(self):
        pass
