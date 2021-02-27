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

from core.badges import badges
from core.tables import tables
from core.session import session

class HatSploitCommand:
    def __init__(self):
        self.badges = badges()
        self.tables = tables()
        self.session = session()

        self.details = {
            'Category': "sessions",
            'Name': "sessions",
            'Description': "Manage opened sessions.",
            'Usage': "sessions [-l|-c <property> <id>]",
            'MinArgs': 1
        }

    def run(self, argc, argv):
        if argv[0] == '-l':
            sessions = self.local_storage.get("sessions")
            
            if sessions:
                for session_property in sessions.keys():
                    sessions_data = list()
                    headers = ("ID", "Host", "Port", "Username", "Hostname")
                    for session_id in sessions[session_property].keys():
                        host = sessions[session_property][session_id]['session_host']
                        port = sessions[session_property][session_id]['session_port']
                        username = sessions[session_property][session_id]['session_username']
                        hostname = sessions[session_property][session_id]['session_hostname']
                        
                        sessions_data.append((session_id, host, port, username, hostname))
                    self.badges.output_empty("")
                    self.tables.print_table("Sessions: " + session_property, headers, *sessions_data)
                    self.badges.output_empty("")
            else:
                self.badges.output_warning("No opened sessions available.")
        elif argv[0] == '-c':
            if argc < 3:
                self.badges.output_usage(self.details['Usage'])
            else:
                if not self.session.close_session(argv[1], argv[2]):
                    self.badges.output_error("Invalid session given!")
        else:
            self.badges.output_usage(self.details['Usage'])
