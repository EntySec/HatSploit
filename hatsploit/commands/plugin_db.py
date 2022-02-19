#!/usr/bin/env python3

#
# This command requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.core.db.builder import Builder
from hatsploit.core.db.db import DB
from hatsploit.lib.command import Command
from hatsploit.lib.show import Show


class HatSploitCommand(Command):
    db = DB()
    builder = Builder()
    show = Show()

    details = {
        'Category': "databases",
        'Name': "plugin_db",
        'Authors': [
            'Ivan Nikolsky (enty8080) - command developer'
        ],
        'Description': "Manage plugin databases.",
        'Usage': "plugin_db <option> [arguments]",
        'MinArgs': 1,
        'Options': {
            '-l': ['', "List all connected plugin databases."],
            '-d': ['<name>', "Disconnect specified plugin database."],
            '-c': ['<name> <path>', "Connect new plugin database."],
            '-b': ['<path> <output_path>', "Build plugin database from plugins path."]
        }
    }

    def run(self, argc, argv):
        choice = argv[1]

        if choice == '-l':
            self.show.show_plugin_databases()
        elif choice == '-d':
            self.db.disconnect_plugin_database(argv[2])
        elif choice == '-b':
            self.builder.build_plugin_database(argv[2], argv[3])
        elif choice == '-c':
            self.db.connect_plugin_database(argv[2], argv[3])
