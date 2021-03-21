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

from core.base.config import Config
from core.base.storage import GlobalStorage
from core.base.storage import LocalStorage
from core.lib.command import Command


class HatSploitCommand(Command):
    config = Config()

    storage_path = config.path_config['base_paths']['storage_path']

    local_storage = LocalStorage()
    global_storage = GlobalStorage(storage_path)

    usage = ""
    usage += "storage [global|local] <option> [arguments]\n\n"
    usage += "  -l, --list                List all storage variables.\n"
    usage += "  -v, --value <name>        Show specified storage variable value.\n"
    usage += "  -s, --set <name> <value>  Set storage veriable value.\n"
    usage += "  -d, --delete <name>       Delete storage variable.\n"

    details = {
        'Category': "developer",
        'Name': "storage",
        'Authors': [
            'enty8080'
        ],
        'Description': "Manage storage variables.",
        'Usage': usage,
        'MinArgs': 2
    }

    def run(self, argc, argv):
        type_of_storage = argv[0]
        if type_of_storage == "global":
            choice = argv[1]
            if choice in ['-l', '--list']:
                self.output_information("Global storage variables:")
                for variable in self.global_storage.get_all():
                    if not str.startswith(variable, '__') and not str.endswith(variable, '__'):
                        self.output_empty("    * " + variable)
            elif choice in ['-v', '--value']:
                if argc < 3:
                    self.output_usage(self.details['Usage'])
                else:
                    if argv[2] in self.global_storage.get_all():
                        self.output_information(argv[2] + " = " + str(
                            self.global_storage.get(argv[2])))
            elif choice in ['-s', '--set']:
                if argc < 4:
                    self.output_usage(self.details['Usage'])
                else:
                    self.global_storage.set(argv[2], argv[3])
            elif choice in ['-d', '--delete']:
                if argc < 3:
                    self.output_usage(self.details['Usage'])
                else:
                    if argv[2] in self.global_storage.get_all():
                        self.global_storage.delete(argv[2])
                    else:
                        self.output_error("Invalid storage variable name!")
            else:
                self.output_usage(self.details['Usage'])
        elif type_of_storage == "local":
            choice = argv[1]
            if choice in ['-l', '--list']:
                self.output_information("Local storage variables:")
                for variable in self.local_storage.get_all():
                    if not str.startswith(variable, '__') and not str.endswith(variable, '__'):
                        self.output_empty("    * " + variable)
            elif choice in ['-v', '--value']:
                if argc < 3:
                    self.output_usage(self.details['Usage'])
                else:
                    if argv[2] in self.local_storage.get_all():
                        self.output_information(argv[2] + " = " + str(
                            self.local_storage.get(argv[2])))
                    else:
                        self.output_error("Invalid storage variable name!")
            elif choice in ['-s', '--set']:
                if argc < 4:
                    self.output_usage(self.details['Usage'])
                else:
                    self.local_storage.set(argv[2], argv[3])
            elif choice in ['-d', '--delete']:
                if argc < 3:
                    self.output_usage(self.details['Usage'])
                else:
                    if argv[2] in self.local_storage.get_all():
                        self.local_storage.delete(argv[2])
                    else:
                        self.output_error("Invalid storage variable name!")
            else:
                self.output_usage(self.details['Usage'])
        else:
            self.output_usage(self.details['Usage'])
