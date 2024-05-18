"""
This command requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.command import Command
from hatsploit.lib.sessions import Sessions
from hatsploit.lib.show import Show


class HatSploitCommand(Command):
    def __init__(self):
        super().__init__()

        self.sessions = Sessions()
        self.show = Show()

        self.details.update({
            'Category': "sessions",
            'Name': "sessions",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - command developer',
            ],
            'Description': "Manage opened sessions.",
            'Usage': "sessions <option> [arguments]",
            'MinArgs': 1,
            'Options': {
                '-l': ['', "List all opened sessions."],
                '-i': ['<id>', "Interact with specified session."],
                '-d': ['<id> <remote_file> <local_path>', "Download file from session."],
                '-u': ['<id> <local_file> <remote_path>', "Upload file to session."],
                '-c': ['<id>', "Close specified session."],
                '--auto-interaction': ['[on|off]', "Interact with session after opening."],
            },
        })

    def run(self, argc, argv):
        if argv[1] == '-l':
            self.show.show_sessions(self.sessions.get_sessions())

        elif argv[1] == '-c':
            self.sessions.close_session(argv[2])

        elif argv[1] == '-i':
            self.sessions.interact_with_session(argv[2])

        elif argv[1] == '-d':
            self.sessions.session_download(argv[2], argv[3], argv[4])

        elif argv[1] == '-u':
            self.sessions.session_upload(argv[2], argv[3], argv[4])

        elif argv[1] == '--auto-interaction':
            if argv[2] == 'on':
                self.sessions.enable_auto_interaction()

            elif argv[2] == 'off':
                self.sessions.disable_auto_interaction()
