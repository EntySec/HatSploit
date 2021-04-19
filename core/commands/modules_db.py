#!/usr/bin/env python3

#
# MIT License
#
# Copyright (c) 2020-2021 EntySec
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

from core.base.storage import LocalStorage
from core.db.db import DB
from core.lib.command import Command


class HatSploitCommand(Command):
    db = DB()
    local_storage = LocalStorage()

    usage = ""
    usage += "modules_db <option> [arguments]\n\n"
    usage += "  -l, --list                   List all connected modules databases.\n"
    usage += "  -d, --disconnect <name>      Disconnect specified modules database.\n"
    usage += "  -c, --connect <name> <path>  Connect new modules database.\n"

    details = {
        'Category': "database",
        'Name': "modules_db",
        'Authors': [
            'Ivan Nikolsky (enty8080)'
        ],
        'Description': "Manage modules databases.",
        'Usage': usage,
        'MinArgs': 1
    }

    def run(self, argc, argv):
        choice = argv[0]
        if choice in ['-l', '--list']:
            if self.local_storage.get("connected_modules_databases"):
                databases_data = list()
                number = 0
                headers = ("Number", "Name", "Path")
                databases = self.local_storage.get("connected_modules_databases")
                for name in databases.keys():
                    databases_data.append((number, name, databases[name]['path']))
                    number += 1
                self.print_table("Connected Modules Databases", headers, *databases_data)
            else:
                self.output_warning("No modules database connected.")
        elif choice in ['-d', '--disconnect']:
            if argc < 2:
                self.output_usage(self.details['Usage'])
            else:
                self.db.disconnect_modules_database(argv[1])
        elif choice in ['-c', '--connect']:
            if argc < 3:
                self.output_usage(self.details['Usage'])
            else:
                self.db.connect_modules_database(argv[1], argv[2])
        else:
            self.output_usage(self.details['Usage'])
