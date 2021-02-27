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

from core.badges import badges
from core.helper import helper
from core.parser import parser

class HatSploitModule:
    def __init__(self):
        self.badges = badges()
        self.helper = helper()
        self.parser = parser()
        
        self.details = {
            'Name': "auxiliary/multi/listener/tcp",
            'Authors': [
                'enty8080'
            ],
            'Description': "Listener for TCP connections.",
            'Dependencies': [
                ''
            ],
            'Comments': [
                ''
            ],
            'Risk': "low"
        }
        
        self.options = {
            'LHOST': {
                'Description': "Local host.",
                'Value': None,
                'Required': True
            },
            'LPORT': {
                'Description': "Local port.",
                'Value': None,
                'Required': True
            }
        }
        
    def run(self):
        local_host, local_port = self.parser.parse_options(self.options)
