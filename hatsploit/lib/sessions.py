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

from hatsploit.core.cli.badges import Badges
from hatsploit.lib.config import Config

from hatsploit.lib.storage import GlobalStorage
from hatsploit.lib.storage import LocalStorage


class Sessions:
    badges = Badges()
    config = Config()

    storage_path = config.path_config['storage_path']

    global_storage = GlobalStorage(storage_path)
    local_storage = LocalStorage()

    def get_sessions(self):
        sessions = self.local_storage.get("sessions")
        return sessions

    def close_dead(self):
        sessions = self.get_sessions()

        if sessions:
            for session in list(sessions):
                if not sessions[session]['Object'].heartbeat():
                    self.badges.print_warning(f"Session {str(session)} is dead (no heartbeat).")
                    self.close_session(session)

    def add_session(self, session_platform, session_architecture,
                    session_type, session_host, session_port, session_object):
        if not self.get_sessions():
            self.local_storage.set("sessions", {})

        session_id = 0
        while (session_id in self.get_sessions() or
               session_id < len(self.get_sessions())):
            session_id += 1

        sessions = {
            session_id: {
                'Platform': session_platform,
                'Architecture': session_architecture,
                'Type': session_type,
                'Host': session_host,
                'Port': session_port,
                'Object': session_object
            }
        }

        self.local_storage.update("sessions", sessions)
        return session_id

    def check_exist(self, session_id, session_platform=None, session_architecture=None, session_type=None):
        sessions = self.get_sessions()

        if sessions:
            if int(session_id) in sessions:
                valid = True

                if session_platform:
                    if sessions[int(session_id)]['Platform'] != session_platform:
                        valid = False

                if session_type:
                    if sessions[int(session_id)]['Type'] != session_type:
                        valid = False

                if session_architecture:
                    if sessions[int(session_id)]['Architecture'] != session_architecture:
                        valid = False

                return valid
        return False

    def enable_auto_interaction(self):
        self.global_storage.set("auto_interaction", True)
        self.global_storage.set_all()

    def disable_auto_interaction(self):
        self.global_storage.set("auto_interaction", False)
        self.global_storage.set_all()

    def interact_with_session(self, session_id):
        sessions = self.get_sessions()

        if self.check_exist(session_id):
            self.badges.print_process(f"Interacting with session {str(session_id)}...%newline")
            sessions[int(session_id)]['Object'].interact()
        else:
            raise RuntimeError("Invalid session given!")

    def session_download(self, session_id, remote_file, local_path):
        sessions = self.get_sessions()

        if self.check_exist(session_id):
            return sessions[int(session_id)]['Object'].download(remote_file, local_path)

        raise RuntimeError("Invalid session given!")

    def session_upload(self, session_id, local_file, remote_path):
        sessions = self.get_sessions()

        if self.check_exist(session_id):
            return sessions[int(session_id)]['Object'].upload(local_file, remote_path)

        raise RuntimeError("Invalid session given!")

    def close_session(self, session_id):
        sessions = self.get_sessions()

        if self.check_exist(session_id):
            try:
                sessions[int(session_id)]['Object'].close()
                del sessions[int(session_id)]

                self.local_storage.update("sessions", sessions)
            except Exception:
                raise RuntimeError("Failed to close session!")
        else:
            raise RuntimeError("Invalid session given!")

    def close_sessions(self):
        sessions = self.get_sessions()

        if sessions:
            for session in list(sessions):
                try:
                    sessions[session]['Object'].close()
                    del sessions[session]

                    self.local_storage.update("sessions", sessions)
                except Exception:
                    raise RuntimeError("Failed to close session!")

    def get_session(self, session_id, session_platform=None, session_architecture=None, session_type=None):
        sessions = self.get_sessions()

        if self.check_exist(session_id, session_platform, session_architecture, session_type):
            return sessions[int(session_id)]['Object']

        raise RuntimeError("Invalid session given!")
