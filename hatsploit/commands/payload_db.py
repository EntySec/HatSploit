"""
This command requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.core.db.builder import Builder
from hatsploit.core.db.db import DB
from badges.cmd import Command
from hatsploit.lib.ui.show import Show


class ExternalCommand(Command):
    def __init__(self):
        super().__init__({
            'Category': "databases",
            'Name': "payload_db",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - command developer',
            ],
            'Description': "Manage payload databases.",
            'Usage': "payload_db <option> [arguments]",
            'MinArgs': 1,
            'Options': {
                'list': ['', "List all connected payload databases."],
                'disconnect': ['<name>', "Disconnect specified payload database."],
                'connect': ['<name> <path>', "Connect new payload database."],
                'build': [
                    '<path> <output_path>',
                    "Build payload database from payloads path.",
                ],
            },
        })

        self.db = DB()
        self.builder = Builder()
        self.show = Show()

    def rpc(self, *args):
        if len(args) < 1:
            return

        if args[0] == 'list':
            return self.db.get_payload_databases()

        elif args[0] == 'disconnect':
            if len(args) >= 2:
                self.db.disconnect_payload_database(args[1])

        elif args[0] == 'build':
            if len(args) >= 3:
                self.builder.build_payload_database(args[1], args[2])

        elif args[0] == 'connect':
            if len(args) >= 3:
                self.db.connect_payload_database(args[1], args[2])

    def run(self, args):
        if args[1] == 'list':
            self.show.show_payload_databases(
                self.db.get_payload_databases())

        elif args[1] == 'disconnect':
            self.db.disconnect_payload_database(args[2])

        elif args[1] == 'build':
            self.builder.build_payload_database(args[2], args[3])

        elif args[1] == 'connect':
            self.db.connect_payload_database(args[2], args[3])
