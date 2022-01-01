#!/usr/bin/env python3

#
# MIT License
#
# Copyright (c) 2020-2022 EntySec
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

import paramiko

from hatsploit.core.cli.badges import Badges


class SSHSocket:
    def __init__(self, host, port, username=None, password=None, timeout=10):
        self.host = host
        self.port = int(port)

        self.username = username
        self.password = password
        self.timeout = timeout

        self.sock = paramiko.SSHClient()
        self.sock.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        self.badges = Badges()

    def connect(self):
        try:
            self.sock.connect(
                self.host,
                port=self.port,
                username=self.username,
                password=self.password,
                timeout=self.timeout
            )

            return True
        except Exception:
            self.badges.print_error(f"Failed to connect to {self.host}!")
        return False

    def disconnect(self):
        try:
            self.sock.close()
            return True
        except Exception:
            self.badges.print_error("Socket is not connected!")
        return False

    def send_command(self, command):
        try:
            return self.sock.exec_command(command)
        except Exception:
            self.badges.print_error("Socket is not connected!")
        return None


class SSHClient:
    @staticmethod
    def open_ssh(host, port, username=None, password=None, timeout=10):
        return SSHSocket(host, port, username, password, timeout)
