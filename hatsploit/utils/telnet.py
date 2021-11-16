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
import sys
import telnetlib
import time

from hatsploit.core.cli.badges import Badges


class TelnetSocket:
    def __init__(self, client):
        self.sock = telnetlib.Telnet()
        self.sock.sock = client

        self.collected = b""
        self.badges = Badges()

    def disconnect(self):
        if self.sock.sock:
            self.sock.close()
            return True
        self.badges.print_error("Socket is not connected!")
        return False

    def send(self, data):
        if self.sock.sock:
            self.sock.write(data)
            return True
        self.badges.print_error("Socket is not connected!")
        return False

    def interact(self, terminator='\n'):
        if self.sock.sock:
            self.badges.print_information("Type %greenquit%end to stop interaction.")
            self.badges.print_empty()

            if self.collected:
                self.badges.print_empty(self.collected.decode(errors='ignore'), start='', end='')
                self.collected = b""

            selector = selectors.SelectSelector()

            selector.register(self.sock, selectors.EVENT_READ)
            selector.register(sys.stdin, selectors.EVENT_READ)

            while True:
                for key, events in selector.select():
                    if key.fileobj is self.sock:
                        try:
                            response = self.sock.read_eager()
                        except Exception:
                            self.badges.print_warning("Connection terminated.")
                            return
                        if response:
                            self.badges.print_empty(response.decode(errors='ignore'), start='', end='')
                    elif key.fileobj is sys.stdin:
                        line = sys.stdin.readline().strip()
                        if not line:
                            pass
                        if line == "quit":
                            return
                        self.sock.write((line + terminator).encode())
        else:
            self.badges.print_error("Socket is not connected!")

    def recv(self, timeout=10):
        if self.sock.sock:
            result = self.collected

            if timeout is not None:
                timeout = time.time() + timeout
                while True:
                    data = self.sock.read_very_eager()
                    result += data

                    if data and not self.collected:
                        self.collected = b""
                        break

                    if time.time() > timeout:
                        self.badges.print_warning("Timeout waiting for response.")
                        return None
            else:
                while True:
                    data = self.sock.read_very_eager()
                    result += data
                    if data:
                        break
            return result
        self.badges.print_error("Socket is not connected!")
        return None

    def send_command(self, command, output=True, timeout=10):
        if self.sock.sock:
            buffer = command.encode()
            self.send(buffer)

            if output:
                try:
                    output = self.recv(timeout)
                    output = output.decode(errors='ignore').strip()

                    return output
                except Exception:
                    self.badges.print_error("Socket is not connected!")
            return None
        self.badges.print_error("Socket is not connected!")
        return None

    def is_terminated(self):
        try:
           self.collected += self.sock.read_eager()
        except Exception:
            return True
        return False


class TelnetClient:
    @staticmethod
    def open_telnet(client):
        return TelnetSocket(client)
