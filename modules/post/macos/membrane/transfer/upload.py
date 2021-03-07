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

from core.lib.module import HatSploitModule
from core.base.sessions import sessions

class HatSploitModule(HatSploitModule):
    sessions = sessions()

    details = {
        'Name': "macOS Membrane Transfer Upload",
        'Module': "post/macos/membrane/transfer/upload",
        'Authors': [
            'enty8080'
        ],
        'Description': "Upload local file.",
        'Dependencies': [
            ''
        ],
        'Comments': [
            ''
        ],
        'Risk': "medium"
    }

    options = {
        'LPATH': {
            'Description': "Local path.",
            'Value': None,
            'Type': None,
            'Required': True
        },
        'RPATH': {
            'Description': "Remote path.",
            'Value': "/tmp",
            'Type': None,
            'Required': True
        },
        'SESSION': {
            'Description': "Session to run on.",
            'Value': 0,
            'Type': "integer",
            'Required': True
        }
    }

    def run(self):
        lpath, rpath, session = self.parser.parse_options(self.options)
        session = self.sessions.get_session("macos/membrane", session)
        if session:
            session.upload(lpath, rpath)
