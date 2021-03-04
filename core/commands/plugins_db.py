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

from core.db.db import db
from core.cli.badges import badges
from core.base.storage import local_storage
from core.cli.tables import tables

class HatSploitCommand:
    def __init__(self):
        self.db = db()
        self.badges = badges()
        self.local_storage = local_storage()
        self.tables = tables()
        
        self.details = {
            'Category': "database",
            'Name': "plugins_db",
            'Description': "Manage plugins databases.",
            'Usage': "plugins_db [-l|-d <name>|-c <name> <path>]",
            'MinArgs': 1
        }

    def run(self, argc, argv):
        choice = argv[0]
        if choice == "-l":
            if self.local_storage.get("connected_plugins_databases"):
                databases_data = list()
                number = 0
                headers = ("Number", "Name", "Path")
                databases = self.local_storage.get("connected_plugins_databases")
                for name in databases.keys():
                    databases_data.append((number, name, databases[name]['path']))
                    number += 1
                self.badges.output_empty("")
                self.tables.print_table("Connected Plugins Databases", headers, *databases_data)
                self.badges.output_empty("")
            else:
                self.badges.output_warning("No plugins database connected.")
        elif choice == '-d':
            if argc < 2:
                self.badges.output_usage(self.details['Usage'])
            else:
                self.db.disconnect_plugins_database(argv[1])
        elif choice == '-c':
            if argc < 3:
                self.badges.output_usage(self.details['Usage'])
            else:
                self.db.connect_plugins_database(argv[1], argv[2])
        else:
            self.badges.output_usage(self.details['Usage'])
