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

from pex.proto.tcp import TCPClient

from pex.proto.tcp import TCPListener
from pex.proto.http import HTTPListener

from hatsploit.core.cli.badges import Badges


class Handle:
    badges = Badges()
    tcp_client = TCPClient()

    tcp_listener = TCPListener()
    http_listener = HTTPListener()

    def listen_server(self, local_host, local_port, methods={}):
        listener = self.http_listener.listen_http(local_host, local_port, methods)

        self.badges.print_process(f"Starting HTTP listener on port {str(local_port)}...")
        listener.listen()

        while True:
            listener.accept()

    def listen_session(self, local_host, local_port, session, timeout=None):
        listener = self.tcp_listener.listen_tcp(local_host, local_port, timeout)

        self.badges.print_process(f"Starting TCP listener on port {str(local_port)}...")

        listener.listen()
        listener.accept()

        address = listener.address

        self.badges.print_process(
            f"Establishing connection ({address[0]}:{str(address[1])} -> {local_host}:{str(local_port)})...")
        listener.stop()

        session = session()
        session.open(listener.client)

        return session, address[0]

    def connect_session(self, remote_host, remote_port, session, timeout=None):
        client = self.tcp_client.open_tcp(remote_host, remote_port, timeout)

        self.badges.print_process(f"Connecting to {local_host}:{str(local_port)}...")
        client.connect()

        self.badges.print_process(
            f"Establishing connection (0.0.0.0:{str(remote_port)} -> {remote_host}:{str(remote_port)})...")
        session = session()
        session.open(client.sock)

        return session
