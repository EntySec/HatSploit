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
from core.lib.command import Command


class HatSploitCommand(Command):
    sessions = Sessions()
    local_storage = LocalStorage()

    usage = ""
    usage += "sessions <option> [arguments]\n\n"
    usage += "  -l, --list [session_platform]                   List all opened sessions\n"
    usage += "                                                  [for specified session platform].\n"
    usage += "  -i, --interact <session_platform> <session_id>  Interact with specified session.\n"
    usage += "  -c, --close <session_platform> <session_id>     Close specified session.\n"

    details = {
        'Category': "sessions",
        'Name': "sessions",
        'Authors': [
            'Ivan Nikolsky (enty8080)'
        ],
        'Description': "Manage opened sessions.",
        'Usage': usage,
        'MinArgs': 1
    }

    def run(self, argc, argv):
        if argv[0] in ['-l', '--list']:
            sessions = self.local_storage.get("sessions")
            if argc < 2:
                if sessions:
                    for session_platform in sessions.keys():
                        sessions_data = list()
                        headers = ("ID", "Type", "Host", "Port")
                        for session_id in sessions[session_platform].keys():
                            session_type = sessions[session_platform][session_id]['type']
                            host = sessions[session_platform][session_id]['host']
                            port = sessions[session_platform][session_id]['port']

                            sessions_data.append((session_id, session_type, host, port))
                        self.print_table("Opened Sessions (" + session_platform + ")", headers, *sessions_data)
                else:
                    self.output_warning("No opened sessions available.")
            else:
                if argv[1] in sessions.keys():
                    session_platform = argv[1]
                    sessions_data = list()
                    headers = ("ID", "Type", "Host", "Port")
                    for session_id in sessions[session_platform].keys():
                        session_type = sessions[session_platform][session_id]['type']
                        host = sessions[session_platform][session_id]['host']
                        port = sessions[session_platform][session_id]['port']

                        sessions_data.append((session_id, session_type, host, port))
                    self.print_table("Opened Sessions (" + session_platform + ")", headers, *sessions_data)
                else:
                    self.output_error("Invalid session platform given!")
        elif argv[0] in ['-c', '--close']:
            if argc < 3:
                self.output_usage(self.details['Usage'])
            else:
                self.sessions.close_session(argv[1], argv[2])
        elif argv[0] in ['-i', '--interact']:
            if argc < 3:
                self.output_usage(self.details['Usage'])
            else:
                self.sessions.spawn_interactive_connection(argv[1], argv[2])
        else:
            self.output_usage(self.details['Usage'])
