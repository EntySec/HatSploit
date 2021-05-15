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

import re
import selectors
import socket
import sys
import telnetlib
import time

from core.utils.tcp.tcp import TCP
from core.base.exceptions import Exceptions
from core.cli.badges import Badges


class TCPClient(TCP):
    badges = Badges()
    exceptions = Exceptions()

    client = None

    def open(self, host, port, timeout=10):
        sock = socket.socket()
        sock.settimeout(timeout)
        sock.connect((host, int(port)))
        return sock

    def connect(self, client):
        self.client = telnetlib.Telnet()
        self.client.sock = client

    def disconnect(self):
        self.client.close()

    def send(self, buffer):
        if self.client:
            self.client.write(buffer)

    def interactive(self, terminator='\n'):
        if self.client:
            selector = selectors.SelectSelector()

            selector.register(self.client, selectors.EVENT_READ)
            selector.register(sys.stdin, selectors.EVENT_READ)

            while True:
                for key, events in selector.select():
                    if key.fileobj is self.client:
                        try:
                            response = self.client.read_eager()
                        except Exception:
                            self.badges.output_warning("Connection terminated.")
                            return
                        if response:
                            self.badges.output_empty(response.decode(), start='', end='')
                    elif key.fileobj is sys.stdin:
                        line = sys.stdin.readline().strip()
                        if not line:
                            pass
                        if line == "exit":
                            return
                        self.client.write((line + terminator).encode())

    def recv(self, timeout=10):
        if self.client:
            result = b""
            if timeout is not None:
                timeout = time.time() + timeout
                while True:
                    data = self.client.read_very_eager()
                    result += data
                    if data:
                        break
                    if time.time() > timeout:
                        raise socket.timeout
            else:
                while True:
                    data = self.client.read_very_eager()
                    result += data
                    if data:
                        break
            return result
        return None

    def send_cmd(self, command, output=True, timeout=10):
        if self.client:
            buffer = command.encode()
            self.send(buffer)

            if output:
                try:
                    output = self.recv(timeout)
                    output = output.decode().strip()

                    return output
                except socket.timeout:
                    self.badges.output_warning("Timeout waiting for response.")
        return None
