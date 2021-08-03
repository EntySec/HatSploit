#!/usr/bin/env python3

#
# This command requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.lib.storage import LocalStorage
from hatsploit.core.db.db import DB
from hatsploit.core.db.builder import Builder
from hatsploit.lib.command import Command


class HatSploitCommand(Command):
    db = DB()
    builder = Builder()
    local_storage = LocalStorage()

    usage = ""
    usage += "plugins_db <option> [arguments]\n\n"
    usage += "  -l, --list                        List all connected plugins databases.\n"
    usage += "  -d, --disconnect <name>           Disconnect specified plugins database.\n"
    usage += "  -c, --connect <name> <path>       Connect new plugins database.\n"
    usage += "  -b, --build <path> <output_path>  Build plugins database from plugins path.\n"

    details = {
        'Category': "databases",
        'Name': "plugins_db",
        'Authors': [
            'Ivan Nikolsky (enty8080) - command developer'
        ],
        'Description': "Manage plugins databases.",
        'Usage': usage,
        'MinArgs': 1
    }

    def run(self, argc, argv):
        choice = argv[0]
        if choice in ['-l', '--list']:
            if self.local_storage.get("connected_plugins_databases"):
                databases_data = list()
                number = 0
                headers = ("Number", "Name", "Path")
                databases = self.local_storage.get("connected_plugins_databases")
                for name in databases.keys():
                    databases_data.append((number, name, databases[name]['path']))
                    number += 1
                self.print_table("Connected Plugins Databases", headers, *databases_data)
            else:
                self.print_warning("No plugins database connected.")
        elif choice in ['-d', '--disconnect']:
            if argc < 2:
                self.print_usage(self.details['Usage'])
            else:
                self.db.disconnect_plugins_database(argv[1])
        elif choice in ['-b', '--build']:
            if argc < 3:
                self.print_usage(self.details['Usage'])
            else:
                self.builder.build_plugins_database(argv[1], argv[2])
        elif choice in ['-c', '--connect']:
            if argc < 3:
                self.print_usage(self.details['Usage'])
            else:
                self.db.connect_plugins_database(argv[1], argv[2])
        else:
            self.print_usage(self.details['Usage'])
