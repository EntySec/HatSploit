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

import requests

from hatsploit.core.cli.badges import Badges
from hatsploit.lib.storage import LocalStorage


class Sessions:
    badges = Badges()
    local_storage = LocalStorage()

    def get_all_sessions(self):
        sessions = self.local_storage.get("sessions")
        return sessions

    def close_dead(self):
        sessions = self.local_storage.get("sessions")
        if sessions:
            for session in list(sessions):
                if not sessions[session]['object'].heartbeat():
                    self.badges.print_warning(f"Session {str(session)} is dead (no heartbeat).")
                    self.close_session(session)
        
    def close_sessions(self):
        if not self.local_storage.get("sessions"):
            return True
        self.badges.print_warning("You have some opened sessions.")
        if self.badges.input_question("Exit anyway? [y/N] ")[0].lower() in ['yes', 'y']:
            self.badges.print_process("Closing all sessions...")
            self.close_all_sessions()
            return True
        return False

    def add_session(self, session_platform, session_architecture, session_type, session_host, session_port, session_object):
        if not self.local_storage.get("sessions"):
            self.local_storage.set("sessions", {})

        session_id = 0
        while (session_id in self.local_storage.get("sessions") or
               session_id < len(self.local_storage.get("sessions"))):
            session_id += 1

        sessions = {
            session_id: {
                'platform': session_platform,
                'architecture': session_architecture,
                'type': session_type,
                'host': session_host,
                'port': session_port,
                'object': session_object
            }
        }

        self.local_storage.update("sessions", sessions)
        return session_id

    def check_exist(self, session_id, session_platform=None, session_architecture=None, session_type=None):
        sessions = self.local_storage.get("sessions")
        if sessions:
            if int(session_id) in sessions:
                valid = True

                if session_platform:
                    if sessions[int(session_id)]['platform'] != session_platform:
                        valid = False

                if session_type:
                    if sessions[int(session_id)]['type'] != session_type:
                        valid = False

                if session_architecture:
                    if sessions[int(session_id)]['architecture'] != session_architecture:
                        valid = False

                return valid
        return False

    def spawn_interactive_connection(self, session_id):
        sessions = self.local_storage.get("sessions")
        if self.check_exist(session_id):
            self.badges.print_process(f"Interacting with session {str(session_id)}...")
            self.badges.print_success("Interactive connection spawned!")

            sessions[int(session_id)]['object'].interact()
        else:
            self.badges.print_error("Invalid session given!")

    def download_from_session(self, session_id, remote_file, local_path):
        sessions = self.local_storage.get("sessions")
        if self.check_exist(session_id):
            sessions[int(session_id)]['object'].download(remote_file, local_path)
        else:
            self.badges.print_error("Invalid session given!")

    def upload_to_session(self, session_id, local_file, remote_path):
        sessions = self.local_storage.get("sessions")
        if self.check_exist(session_id):
            sessions[int(session_id)]['object'].upload(local_file, remote_path)
        else:
            self.badges.print_error("Invalid session given!")

    def close_session(self, session_id):
        sessions = self.local_storage.get("sessions")
        if self.check_exist(session_id):
            try:
                sessions[int(session_id)]['object'].close()
                del sessions[int(session_id)]

                self.local_storage.update("sessions", sessions)
            except Exception:
                self.badges.print_error("Failed to close session!")
        else:
            self.badges.print_error("Invalid session given!")

    def close_all_sessions(self):
        sessions = self.local_storage.get("sessions")
        if sessions:
            for session in list(sessions):
                try:
                    sessions[session]['object'].close()
                    del sessions[session]

                    self.local_storage.update("sessions", sessions)
                except Exception:
                    self.badges.print_error("Failed to close session!")

    def get_session(self, session_id, session_platform=None, session_architecture=None, session_type=None):
        sessions = self.local_storage.get("sessions")
        if self.check_exist(session_id, session_platform, session_architecture, session_type):
            return sessions[int(session_id)]['object']
        self.badges.print_error("Invalid session given!")
        return None
