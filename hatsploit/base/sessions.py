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

from hatsploit.base.storage import LocalStorage
from hatsploit.core.cli.badges import Badges


class Sessions:
    def __init__(self):
        self.badges = Badges()
        self.local_storage = LocalStorage()

    def get_all_sessions(self):
        sessions = self.local_storage.get("sessions")
        return sessions

    def add_session(self, session_platform, session_type, session_host, session_port, session_object):
        if not self.local_storage.get("sessions"):
            self.local_storage.set("sessions", dict())

        session_id = 0
        if session_platform in self.local_storage.get("sessions").keys():
            sessions = self.local_storage.get("sessions")
            session_id = len(sessions[session_platform])
            sessions[session_platform][int(session_id)] = {
                'type': session_type,
                'host': session_host,
                'port': session_port,
                'object': session_object
            }
        else:
            sessions = {
                session_platform: {
                    int(session_id): {
                        'type': session_type,
                        'host': session_host,
                        'port': session_port,
                        'object': session_object
                    }
                }
            }

        self.local_storage.update("sessions", sessions)
        return session_id

    def check_session_exist(self, session_platform, session_id):
        sessions = self.local_storage.get("sessions")
        if sessions:
            if session_platform in sessions.keys():
                if int(session_id) in sessions[session_platform].keys():
                    return True
        return False

    def spawn_interactive_connection(self, session_platform, session_id):
        sessions = self.local_storage.get("sessions")
        if self.check_session_exist(session_platform, session_id):
            self.badges.output_process("Interacting with session " + str(session_id) + "...")
            self.badges.output_success("Interactive connection spawned!")
            self.badges.output_information("Type commands below.\n")

            sessions[session_platform][int(session_id)]['object'].interact()
        else:
            self.badges.output_error("Invalid session given!")

    def close_session(self, session_platform, session_id):
        sessions = self.local_storage.get("sessions")
        if self.check_session_exist(session_platform, session_id):
            try:
                sessions[session_platform][int(session_id)]['object'].close()
                del sessions[session_platform][int(session_id)]

                if not sessions[session_platform]:
                    del sessions[session_platform]
                self.local_storage.update("sessions", sessions)
            except Exception:
                self.badges.output_error("Failed to close session!")
        else:
            self.badges.output_error("Invalid session given!")

    def get_session(self, session_platform, session_type, session_id):
        sessions = self.local_storage.get("sessions")
        if self.check_session_exist(session_platform, session_id):
            if session_type == sessions[session_platform][int(session_id)]['type']:
                return sessions[session_platform][int(session_id)]['object']
            self.badges.output_error("Session with invalid type!")
            return None
        return None
