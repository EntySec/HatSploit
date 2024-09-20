"""
This command requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

import os

from badges.cmd import Command

from hatsploit.lib.ui.sessions import Sessions
from hatsploit.lib.ui.show import Show


class ExternalCommand(Command):
    def __init__(self):
        super().__init__({
            'Category': "manage",
            'Name': "sessions",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - command developer',
            ],
            'Description': "Manage opened sessions.",
            'MinArgs': 1,
            'Options': [
                (
                    ('-l', '--list'),
                    {
                        'help': "List all opened sessions.",
                        'action': 'store_true'
                    }
                ),
                (
                    ('-s', '--session'),
                    {
                        'help': 'Opened session by ID to manage.',
                        'metavar': 'ID',
                        'type': int
                    }
                ),
                (
                    ('-c', '--close'),
                    {
                        'help': "Close specified session.",
                        'action': 'store_true'
                    }
                ),
                (
                    ('-i', '--interact'),
                    {
                        'help': "Interact specified session.",
                        'action': 'store_true'
                    }
                ),
                (
                    ('-d', '--download'),
                    {
                        'help': "Download file from session.",
                        'metavar': 'REMOTE_FILE',
                    }
                ),
                (
                    ('-u', '--upload'),
                    {
                        'help': "Upload file to session.",
                        'metavar': 'LOCAL_FILE',
                    }
                ),
                (
                    ('-o', '--output'),
                    {
                        'help': 'Path to save downloaded/uploaded file.',
                        'metavar': 'PATH'
                    }
                ),
                (
                    ('-A', '--auto-interaction'),
                    {
                        'help': 'Disable/enable auto-interaction.',
                        'choices': ['on', 'off'],
                        'dest': 'autoflag'
                    }
                )
            ]
        })

        self.sessions = Sessions()
        self.show = Show()

    def run(self, args):
        if args.list:
            self.show.show_sessions(self.sessions.get_sessions())
            return

        if args.autoflag:
            if args.autoflags == 'yes':
                self.sessions.enable_auto_interaction()
            else:
                self.sessions.disable_auto_interaction()

            return

        if args.session is None:
            self.print_warning("No session specified.")
            return

        if args.close:
            self.sessions.close_session(args.session)
            return

        if args.interact:
            self.sessions.interact_with_session(args.session)
            return

        if args.download:
            self.sessions.session_download(
                args.session, args.download,
                args.output or os.path.split(args.download)[1])
            return

        if args.upload:
            self.sessions.session_upload(
                args.session, args.upload,
                args.output or os.path.split(args.upload)[1])

        else:
            return True
