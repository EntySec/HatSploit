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
from core.cli.parser import parser
from core.base.sessions import sessions

class HatSploitModule:
    def __init__(self):
        self.badges = badges()
        self.parser = parser()
        self.sessions = sessions()

        self.details = {
            'Name': "macOS Membrane Gather Volume",
            'Module': "post/macos/membrane/gather/getvol",
            'Authors': [
                'enty8080'
            ],
            'Description': "Get device volume level.",
            'Dependencies': [
                ''
            ],
            'Comments': [
                ''
            ],
            'Risk': "medium"
        }

        self.options = {
            'SESSION': {
                'Description': "Session to run on.",
                'Value': 0,
                'Types': [
                    int
                ],
                'Required': True
            }
        }

    def run(self):
        session = self.sessions.get_session("macos/membrane", self.parser.parse_options(self.options))
        if session:
            self.badges.output_process("Getting device volume level...")
            payload = "output volume of (get volume settings)"

            status, output = session.send_command("osascript", payload)
            if not status:
                self.badges.output_error("Failed to get device volume level!")
            else:
                self.badges.output_information("Volume Level: " + output)
