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
        'Name': "encoder_db",
        'Authors': [
            'Ivan Nikolsky (enty8080) - command developer'
        ],
        'Description': "Manage encoder databases.",
        'Usage': "encoder_db <option> [arguments]",
        'MinArgs': 1,
        'Options': {
            '-l': ['', "List all connected encoder databases."],
            '-d': ['<name>', "Disconnect specified encoder database."],
            '-c': ['<name> <path>', "Connect new encoder database."],
            '-b': ['<path> <output_path>', "Build encoder database from encoders path."]
        }
    }

    def run(self, argc, argv):
        choice = argv[1]

        if choice == '-l':
            self.show.show_encoder_databases()
        elif choice == '-d':
            self.db.disconnect_encoder_database(argv[2])
        elif choice == '-b':
            self.builder.build_encoder_database(argv[2], argv[3])
        elif choice == '-c':
            self.db.connect_encoder_database(argv[2], argv[3])
