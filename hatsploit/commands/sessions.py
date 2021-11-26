#!/usr/bin/env python3

#
# This command requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.lib.command import Command
from hatsploit.lib.sessions import Sessions
from hatsploit.lib.show import Show


class HatSploitCommand(Command):
    sessions = Sessions()
    show = Show()

    usage = ""
    usage += "sessions <option> [arguments]\n\n"
    usage += "  -l, --list                                              List all opened sessions.\n"
    usage += "  -i, --interact <session_id>                             Interact with specified session.\n"
    usage += "  -d, --download <session_id> <remote_file> <local_path>  Download file from session.\n"
    usage += "  -u, --upload <session_id> <local_file> <remote_path>    Upload file to session.\n"
    usage += "  -c, --close <session_id>                                Close specified session.\n"

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
        if argv[1] in ['-l', '--list']:
            self.show.show_sessions()
        elif argv[1] in ['-c', '--close']:
            if argc < 3:
                self.print_usage(self.details['Usage'])
            else:
                self.sessions.close_session(argv[2])
        elif argv[1] in ['-i', '--interact']:
            if argc < 3:
                self.print_usage(self.details['Usage'])
            else:
                self.sessions.spawn_interactive_connection(argv[2])
        elif argv[1] in ['-d', '--download']:
            if argv < 5:
                self.print_usage(self.details['Usage'])
            else:
                self.sessions.download_from_session(argv[2], argv[3], argv[4])
        elif argv[1] in ['-u', '--upload']:
            if argv < 5:
                self.print_usage(self.details['Usage'])
            else:
                self.sessions.upload_to_session(argv[2], argv[3], argv[4])
        else:
            self.print_usage(self.details['Usage'])
