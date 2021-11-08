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

    usage = ""
    usage += "payload_db <option> [arguments]\n\n"
    usage += "  -l, --list                        List all connected payload databases.\n"
    usage += "  -d, --disconnect <name>           Disconnect specified payload database.\n"
    usage += "  -c, --connect <name> <path>       Connect new payload database.\n"
    usage += "  -b, --build <path> <output_path>  Build payload database from payloads path.\n"

    details = {
        'Category': "databases",
        'Name': "payload_db",
        'Authors': [
            'Ivan Nikolsky (enty8080) - command developer'
        ],
        'Description': "Manage payload databases.",
        'Usage': usage,
        'MinArgs': 1
    }

    def run(self, argc, argv):
        choice = argv[1]
        if choice in ['-l', '--list']:
            self.show.show_payload_databases()
        elif choice in ['-d', '--disconnect']:
            if argc < 3:
                self.print_usage(self.details['Usage'])
            else:
                self.db.disconnect_payloads_database(argv[2])
        elif choice in ['-b', '--build']:
            if argc < 4:
                self.print_usage(self.details['Usage'])
            else:
                self.builder.build_payloads_database(argv[2], argv[3])
        elif choice in ['-c', '--connect']:
            if argc < 4:
                self.print_usage(self.details['Usage'])
            else:
                self.db.connect_payloads_database(argv[2], argv[3])
        else:
            self.print_usage(self.details['Usage'])
