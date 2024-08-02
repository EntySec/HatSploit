"""
This command requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from badges.cmd import Command
from hatsploit.lib.ui.sessions import Sessions
from hatsploit.lib.ui.show import Show


class ExternalCommand(Command):
    def __init__(self):
        super().__init__({
            'Category': "sessions",
            'Name': "sessions",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - command developer',
            ],
            'Description': "Manage opened sessions.",
            'Usage': "sessions <option> [arguments]",
            'MinArgs': 1,
            'Options': {
                'list': ['', "List all opened sessions."],
                'interact': ['<id>', "Interact with specified session."],
                'download': ['<id> <remote_file> <local_path>', "Download file from session."],
                'upload': ['<id> <local_file> <remote_path>', "Upload file to session."],
                'close': ['<id>', "Close specified session."],
                'auto-interaction': ['[on|off]', "Interact with session after opening."],
            },
        })

        self.sessions = Sessions()
        self.show = Show()

    def run(self, args):
        if args[1] == 'list':
            self.show.show_sessions(self.sessions.get_sessions())

        elif args[1] == 'close':
            self.sessions.close_session(args[2])

        elif args[1] == 'interact':
            self.sessions.interact_with_session(args[2])

        elif args[1] == 'download':
            self.sessions.session_download(args[2], args[3], args[4])

        elif args[1] == 'upload':
            self.sessions.session_upload(args[2], args[3], args[4])

        elif args[1] == 'auto-interaction':
            if args[2] == 'on':
                self.sessions.enable_auto_interaction()

            elif args[2] == 'off':
                self.sessions.disable_auto_interaction()
