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

import ipaddress
import requests

from hatsploit.lib.storage import LocalStorage
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
        while (session_id in self.local_storage.get("sessions") or
               session_id < len(self.local_storage.get("sessions"))):
            session_id += 1

        session_latitude = '0'
        session_longitude = '0'

        try:
            if ipaddress.ip_address(session_host).is_private:
                data = requests.get("https://www.myexternalip.com/json", timeout=3).json()
                host = data['ip']
            else:
                host = session_host

            data = requests.get(f"http://ipinfo.io/{host}", timeout=3).json()['loc'].split(',')

            session_latitude = data[0]
            session_longitude = data[1]
        except Exception:
            pass

        sessions = {
            session_id: {
                'platform': session_platform,
                'type': session_type,
                'host': session_host,
                'port': session_port,
                'latitude': session_latitude,
                'longitude': session_longitude,
                'object': session_object
            }
        }

        self.local_storage.update("sessions", sessions)
        return session_id

    def check_exist(self, session_id, session_platform=None, session_type=None):
        sessions = self.local_storage.get("sessions")
        if sessions:
            if int(session_id) in sessions.keys():
                if session_platform and session_type:
                    if (sessions[int(session_id)]['platform'] == session_platform and
                        sessions[int(sessions_id)]['type'] == session_type):
                        return True
                    return False
                if session_platform:
                    if sessions[int(session_id)]['platform'] == session_platform:
                        return True
                    return False
                if session_type:
                    if sessions[int(sessions_id)]['type'] == session_type:
                        return True
                    return False
                return True
        return False

    def spawn_interactive_connection(self, session_id):
        sessions = self.local_storage.get("sessions")
        if self.check_exist(session_id):
            self.badges.print_process("Interacting with session " + str(session_id) + "...")
            self.badges.print_success("Interactive connection spawned!")
            self.badges.print_information("Type commands below.\n")

            sessions[int(session_id)]['object'].interact()
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
            for session in sessions:
                try:
                    sessions[session]['object'].close()
                    del sessions[session]

                    self.local_storage.update("sessions", sessions)
                except Exception:
                    self.badges.print_error("Failed to close session!")

    def get_session(self, session_id):
        sessions = self.local_storage.get("sessions")
        if self.check_exist(session_id):
            return sessions[int(session_id)]['object']
        return None
