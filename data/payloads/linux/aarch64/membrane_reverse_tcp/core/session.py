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

from core.lib.session import session

from utils.tcp.tcp import tcp

from data.payloads.linux.aarch64.membrane_reverse_tcp.core.transfer import transfer

class session(session):
    def __init__(self, client):
        self.tcp = tcp()

        self.transfer = transfer(client)
        self.tcp.connect(client)

    details = {
        'Platform': "linux",
        'Type': "membrane"
    }

    def close(self):
        self.tcp.disconnect()

    def send_command(self, command, arguments=None, timeout=10):
        if arguments:
            command += " " + arguments

        output = self.tcp.send_command(command + '\x04', timeout)

        if "error" in output:
            return (False, "")
        return (True, output)

    def interact(self):
        self.tcp.interactive('\x04')
    
    def download(self, input_file, output_path):
        self.transfer.download(input_file, output_path)

    def upload(self, input_file, output_path):
        self.transfer.upload(input_file, output_path)
