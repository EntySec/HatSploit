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
            'Options': [
                (
                    ('-t', '--table'),
                    {
                        'help': 'Table to use for DB.',
                        'choices': ('modules', 'plugins', 'payloads', 'encoders'),
                        'required': True
                    }
                ),
                (
                    ('-b', '--build'),
                    {
                        'help': 'Build database to output path.',
                    }
                )
            ]
        })

    def run(self, args):
        if args.build:
            db = DB(table=args.table)
            db.build(args.build)

            return

        return True
