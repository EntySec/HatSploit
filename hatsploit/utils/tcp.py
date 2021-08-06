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

import socket

from hatsploit.core.cli.badges import Badges


class TCPSocket:
    def __init__(self, host, port, timeout=10):
        self.host = host
        self.port = int(port)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(timeout)

        self.badges = Badges()

    def connect(self):
        try:
            self.sock.connect((self.host, self.port))
            return True
        except Exception:
            self.badges.print_error("Failed to connect!")
        return False

    def disconnect(self):
        try:
            self.sock.close()
            return True
        except Exception:
            self.badges.print_error("Socket is not connected!")
        return False

    def send(self, data):
        try:
            self.sock.send(data)
            return True
        except Exception:
            self.badges.print_error("Socket is not connected!")
        return False

    def recv(self, size):
        try:
            return self.sock.recv(size)
        except Exception:
            self.badges.print_error("Socket is not connected!")
        return b""


class TCPClient:
    @staticmethod
    def get_local_host():
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            server.connect(("8.8.8.8", 53))
            local_host = server.getsockname()[0]
            server.close()
            local_host = local_host
        except Exception:
            local_host = "127.0.0.1"
        return local_host

    def convert_to_local(self, host):
        if host in ['0.0.0.0']:
            return self.get_local_host()
        return host

    @staticmethod
    def check_tcp_port(host, port, timeout=0.5):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            if sock.connect_ex((host, int(port))) == 0:
                return True
        return False

    @staticmethod
    def open_tcp(host, port, timeout=10):
        return TCPSocket(host, port, timeout)
