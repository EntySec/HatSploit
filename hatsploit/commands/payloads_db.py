#!/usr/bin/env python3

#
# This command requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.core.base.storage import LocalStorage
from hatsploit.core.db.db import DB
from hatsploit.command import Command


class HatSploitCommand(Command):
    db = DB()
    local_storage = LocalStorage()

    usage = ""
    usage += "payloads_db <option> [arguments]\n\n"
    usage += "  -l, --list                   List all connected payloads databases.\n"
    usage += "  -d, --disconnect <name>      Disconnect specified payloads database.\n"
    usage += "  -c, --connect <name> <path>  Connect new payloads database.\n"

    details = {
        'Category': "database",
        'Name': "payloads_db",
        'Authors': [
            'Ivan Nikolsky (enty8080)'
        ],
        'Description': "Manage payloads databases.",
        'Usage': usage,
        'MinArgs': 1
    }

    def run(self, argc, argv):
        choice = argv[0]
        if choice in ['-l', '--list']:
            if self.local_storage.get("connected_payloads_databases"):
                databases_data = list()
                number = 0
                headers = ("Number", "Name", "Path")
                databases = self.local_storage.get("connected_payloads_databases")
                for name in databases.keys():
                    databases_data.append((number, name, databases[name]['path']))
                    number += 1
                self.print_table("Connected Payloads Databases", headers, *databases_data)
            else:
                self.output_warning("No payloads database connected.")
        elif choice in ['-d', '--disconnect']:
            if argc < 2:
                self.output_usage(self.details['Usage'])
            else:
                self.db.disconnect_payloads_database(argv[1])
        elif choice in ['-c', '--connect']:
            if argc < 3:
                self.output_usage(self.details['Usage'])
            else:
                self.db.connect_payloads_database(argv[1], argv[2])
        else:
            self.output_usage(self.details['Usage'])
