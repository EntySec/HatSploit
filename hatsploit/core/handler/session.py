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

from hatsploit.utils.fs import FSTools
from hatsploit.utils.telnet import TelnetClient


class HatSploitSession(Session, FSTools, TelnetClient):
    client = None

    details = {
        'Platform': "",
        'Type': "shell"
    }

    def open(self, client):
        self.client = self.open_telnet(client)

    def close(self):
        self.client.disconnect()

    def heartbeat(self):
        return not self.client.terminated

    def send_command(self, command, output=False, timeout=10):
        output = self.client.send_command(command + '\n', output, timeout)
        return output

    def download(self, remote_file, local_path, timeout=None):
        if self.details['Platform'] != 'windows':
            command = f"cat \"{remote_file}\""
        else:
            command = ""

        exists, is_dir = self.exists_directory(local_file)

        if exists:
            if is_dir:
                local_file = local_file + '/' + os.path.split(remote_file)[1]

            data = self.client.send_command(command + '\n', True, timeout, True)

            with open(local_file, 'wb'):
                f.write(data)

            self.print_success("File has been downloaded!")
        else:
            self.print_error("Failed to download file!")

    def interact(self):
        self.client.interact()
