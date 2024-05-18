"""
This command requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.core.db.builder import Builder
from hatsploit.core.db.db import DB
from hatsploit.lib.command import Command
from hatsploit.lib.show import Show


class HatSploitCommand(Command):
    def __init__(self):
        super().__init__()

        self.db = DB()
        self.builder = Builder()
        self.show = Show()

        self.details.update({
            'Category': "databases",
            'Name': "plugin_db",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - command developer',
            ],
            'Description': "Manage plugin databases.",
            'Usage': "plugin_db <option> [arguments]",
            'MinArgs': 1,
            'Options': {
                '-l': ['', "List all connected plugin databases."],
                '-d': ['<name>', "Disconnect specified plugin database."],
                '-c': ['<name> <path>', "Connect new plugin database."],
                '-b': ['<path> <output_path>', "Build plugin database from plugins path."],
            },
        })

    def rpc(self, *args):
        if len(args) < 1:
            return

        if args[0] == 'list':
            return self.db.get_plugin_databases()

        elif args[0] == 'disconnect':
            if len(args) >= 2:
                self.db.disconnect_plugin_database(args[1])

        elif args[0] == 'build':
            if len(args) >= 3:
                self.builder.build_plugin_database(args[1], args[2])

        elif args[0] == 'connect':
            if len(args) >= 3:
                self.db.connect_plugin_database(args[1], args[2])

    def run(self, argc, argv):
        choice = argv[1]

        if choice == '-l':
            self.show.show_plugin_databases(
                self.db.get_plugin_databases())

        elif choice == '-d':
            self.db.disconnect_plugin_database(argv[2])

        elif choice == '-b':
            self.builder.build_plugin_database(argv[2], argv[3])

        elif choice == '-c':
            self.db.connect_plugin_database(argv[2], argv[3])
