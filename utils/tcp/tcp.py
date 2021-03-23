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

from core.base.exceptions import Exceptions
from core.cli.badges import Badges


class TCPClient:
    badges = Badges()
    exceptions = Exceptions()

    client = None

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
        if sock.connect_ex((host, int(port))) == 0:
            sock.close()
            return True
        sock.close()
        return False

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

    def send_cmd(self, command, timeout=10):
        if self.client:
            buffer = command.encode()
            self.send(buffer)

            output = self.recv(timeout)
            output = output.decode().strip()

            return output
        return None

    def start_server(self, local_host, local_port):
        address = local_host + ':' + str(local_port)
        self.badges.output_process("Binding to " + address + "...")
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind((local_host, int(local_port)))
            server.listen(1)
        except Exception:
            self.badges.output_error("Failed to bind to " + address + "!")
            raise self.exceptions.GlobalException
        return server

    def connect_server(self, remote_host, remote_port, timeout=None):
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
            raise self.exceptions.GlobalException
        except Exception:
            self.badges.output_error("Failed to listen on port " + str(local_port) + "!")
            raise self.exceptions.GlobalException
        return client, address[0]
