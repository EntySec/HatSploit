"""
This command requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.core.db.db import DB
from badges.cmd import Command


class ExternalCommand(Command):
    def __init__(self):
        super().__init__({
            'Category': "manage",
            'Name': "db",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - command developer',
            ],
            'Description': "Manage database.",
            'Usage': "db <option> [arguments]",
            'MinArgs': 1,
            'Options': {
                'build': [
                    '[modules|plugins|payloads|encoders] <path>',
                    "Build database from path."
                ],
            },
        })

    def rpc(self, *args):
        if len(args) < 1:
            return

        elif args[0] == 'build':
            if len(args) >= 3:
                db = DB(table=args[1])
                db.build(args[2])

    def run(self, args):
        if args[1] == 'build':
            db = DB(table=args[2])
            db.build(args[3])
