#!/usr/bin/env python3

#
# This command requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.lib.command import Command
from hatsploit.lib.sessions import Sessions
from hatsploit.lib.storage import LocalStorage


class HatSploitCommand(Command):
    sessions = Sessions()
    local_storage = LocalStorage()

    usage = ""
    usage += "sessions <option> [arguments]\n\n"
    usage += "  -l, --list                   List all opened sessions.\n"
    usage += "  -i, --interact <session_id>  Interact with specified session.\n"
    usage += "  -c, --close <session_id>     Close specified session.\n"

    details = {
        'Category': "sessions",
        'Name': "sessions",
        'Authors': [
            'Ivan Nikolsky (enty8080) - command developer'
        ],
        'Description': "Manage opened sessions.",
        'Usage': usage,
        'MinArgs': 1
    }

    def run(self, argc, argv):
        if argv[0] in ['-l', '--list']:
            sessions = self.local_storage.get("sessions")
            if sessions:
                sessions_data = list()
                headers = ("ID", "Platform", "Type", "Host", "Port")
                for session_id in sessions.keys():
                    session_platform = sessions[session_id]['platform']
                    session_type = sessions[session_id]['type']
                    host = sessions[session_id]['host']
                    port = sessions[session_id]['port']

                    sessions_data.append((session_id, session_platform, session_type, host, port))
                self.print_table("Opened Sessions", headers, *sessions_data)
            else:
                self.print_warning("No opened sessions available.")
        elif argv[0] in ['-c', '--close']:
            if argc < 2:
                self.print_usage(self.details['Usage'])
            else:
                self.sessions.close_session(argv[1])
        elif argv[0] in ['-i', '--interact']:
            if argc < 2:
                self.print_usage(self.details['Usage'])
            else:
                self.sessions.spawn_interactive_connection(argv[1])
        else:
            self.print_usage(self.details['Usage'])
