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

from core.cli.badges import Badges
from core.base.exceptions import Exceptions


class TCP:
    def __init__(self):
        self.badges = Badges()
        self.exceptions = Exceptions()

    @staticmethod
    def get_local_host():
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            server.connect(("192.168.1.1", 80))
            local_host = server.getsockname()[0]
            server.close()
            local_host = local_host
        except Exception:
            local_host = "127.0.0.1"
        return local_host

    @staticmethod
    def tcp_request(host, port, data, buffer_size=1024, timeout=10):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((host, int(port)))
        sock.send(data.encode())
        output = sock.recv(buffer_size)
        sock.close()
        return output.decode().strip()

    @staticmethod
    def check_tcp_port(host, port, timeout=10):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        try:
            sock = sock.connect((host, int(port)))
            sock.close()
            return True
        except:
            return False

    def connect(self, remote_host, remote_port, timeout=None):
        address = remote_host + ':' + str(remote_port)
        self.badges.output_process("Connecting to " + address + "...")
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.settimeout(timeout)

            server.connect((remote_host, int(remote_port)))
            self.badges.output_process("Establishing connection...")
        except socket.timeout:
            self.badges.output_warning("Connection timeout.")
            raise self.exceptions.GlobalException
        except Exception:
            self.badges.output_error("Failed to connect to " + address + "!")
            raise self.exceptions.GlobalException
        return server

    def listen(self, local_host, local_port, timeout=None):
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.settimeout(timeout)
            server.bind((local_host, int(local_port)))
            server.listen(1)

            self.badges.output_process("Listening on port " + str(local_port) + "...")
            client, address = server.accept()
            self.badges.output_process("Connecting to " + address[0] + "...")
            self.badges.output_process("Establishing connection...")

            server.close()
        except socket.timeout:
            self.badges.output_warning("Timeout waiting for connection.")

            server.close()
            raise self.exceptions.GlobalException
        except Exception:
            self.badges.output_error("Failed to listen on port " + str(local_port) + "!")
            raise self.exceptions.GlobalException
        return client, address[0]
