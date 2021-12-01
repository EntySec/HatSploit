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

from hatsploit.lib.session import Session

from hatsploit.core.session.pull import Pull
from hatsploit.core.session.push import Push

from hatsploit.utils.telnet import TelnetClient


class HatSploitSession(Session, Pull, Push, TelnetClient):
    client = None

    details = {
        'Post': "",
        'Platform': "",
        'Type': "shell"
    }

    def open(self, client):
        self.client = self.open_telnet(client)

    def close(self):
        self.client.disconnect()

    def heartbeat(self):
        return not self.client.terminated

    def send_command(self, command, output=False, decode=True):
        return self.client.send_command(
            (command + '\n'),
            output,
            decode
        )

    def download(self, remote_file, local_path):
        return self.pull(
            remote_file,
            self.send_command,
            local_path,
            {
                'decode': False,
                'output': True
            }
        )

    def upload(self, local_file, remote_path):
        return self.push(
            local_file,
            self.send_command,
            remote_path
        )

    def interact(self):
        self.client.interact()
