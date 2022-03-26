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

from pex.client.tcp import TCPClient
from pex.listener.tcp import TCPListener

from hatsploit.core.cli.badges import Badges


class Handle(TCPClient, TCPListener):
    def listen_session(self, local_host, local_port, session, timeout=None):
        listener = self.listen_tcp(local_host, local_port, timeout)

        if listener.listen():
            self.badges.print_process(f"Starting TCP listener on port {str(local_port)}...")
            client, address = listener.accept()

            self.badges.print_process(f"Establishing connection ({address[0]}:{address[1]} -> {local_host}:{local_port})...")
            listener.stop()

            if client and address:
                session = session()
                session.open(client)

                return session, address

            self.badges.print_warning("Timeout waiting for connection.")
        else:
            self.badges.print_error(f"Failed to start TCP listener on port {str(local_port)}!")

        self.badges.print_error("Failed to handle session!")
        return None, None

    def connect_session(self, remote_host, remote_port, session, timeout=None):
        client = self.open_tcp(remote_host, remote_port, timeout)

        if client.connect():
            session = session()
            session.open(client)

            return session

        self.badges.print_error("Failed to handle session!")
        return None
