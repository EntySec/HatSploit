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

from core.base.sessions import sessions
from core.base.storage import local_storage
from core.cli.badges import badges

from utils.tcp.tcp import tcp

from data.utils.handler.handler.session import session

class handler:
    def __init__(self):
        self.sessions = sessions()
        self.local_storage = local_storage()
        self.exceptions = exceptions()
        self.badges = badges()

        self.tcp = tcp()
        
        self.server = None

    def start_handler(self, local_host, local_port):
        if self.tcp.check_tcp_port(local_port):
            self.badges.output_error("Provided port is already in use!")
        else:
            self.badges.output_process("Starting reverse TCP handler on port " + str(local_port) + "...")
            try:
                self.server = self.tcp.start_server(local_host, local_port)
                self.badges.output_success("Reverse TCP handler successfully started!")
                return True
            except Exception:
                self.badges.output_error("Failed to start reverse TCP handler!")
        return False

    def listen_for_session(self, server, local_host, local_port, session=session):
        try:
            client, address = server.accept()
            self.badges.output_process("Connecting to " + address[0] + "...")
            self.badges.output_process("Establishing connection...")
            session = session(client)
            return (session, address[0])
        except Exception:
            self.badges.output_error("Failed to listen!")
            return (None, None)

    def handle_session(self, module_name, session_property, local_host, local_port, session=session):
        if self.server:
            session, address = self.listen_for_session(self.server, local_host, local_port, session)
            if not session and not address:
                return False

            session_id = self.sessions.add_session(session_property, module_name, address, local_port, session)
            self.badges.output_success("Session " + str(session_id) + " opened!")
            return True
        return False
