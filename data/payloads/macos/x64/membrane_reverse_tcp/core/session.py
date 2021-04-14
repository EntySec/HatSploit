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

from core.lib.session import Session
from utils.tcp.tcp import TCPClient

class HatSploitSession(Session, TCPClient):
    details = {
        'Platform': "macos",
        'Type': "membrane"
    }

    def open(self, client):
        self.connect(client)

    def close(self):
        self.disconnect()

    def send_command(self, command, arguments=None, output=True, timeout=None):
        if arguments:
            command += " " + arguments

        output = self.send_cmd(command + '\n', output, timeout)
        output = output.replace('\nmembrane% ', "")

        if "Unrecognized command:" in output:
            return False, ""
        return True, output

    def interact(self):
        self.interactive()
