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
import sys

import socket

from core.badges import badges
from core.parser import parser

from utils.web_tools import web_tools

class HatSploitModule:
    def __init__(self):
        self.badges = badges()
        self.parser = parser()
        
        self.web_tools = web_tools()

        self.details = {
            'Name': "auxiliary/android/checker/check_adb_installation",
            'Authors': [
                'enty8080'
            ],
            'Description': "Check if remote Android device has ADB installation.",
            'Dependencies': [
                ''
            ],
            'Comments': [
                ''
            ],
            'Risk': "low"
        }

        self.options = {
            'RHOST': {
                'Description': "Remote host.",
                'Value': None,
                'Required': True
            }
        }

    def run(self):
        remote_host = self.parser.parse_options(self.options)
        
        self.badges.output_process("Checking " + remote_host + "...")
        
        if self.web_tools.check_tcp_port(remote_host, 5555):
            self.badges.output_success("Target device may has ADB installation!")
        else:
            self.badges.output_warning("Looks like target device has no ADB installation.")
        checker.close()
