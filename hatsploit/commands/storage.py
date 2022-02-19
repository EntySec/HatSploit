#!/usr/bin/env python3

#
# This command requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.lib.command import Command
from hatsploit.lib.config import Config
from hatsploit.lib.storage import GlobalStorage
from hatsploit.lib.storage import LocalStorage


class HatSploitCommand(Command):
    config = Config()

    storage_path = config.path_config['storage_path']

    local_storage = LocalStorage()
    global_storage = GlobalStorage(storage_path)

    details = {
        'Category': "developer",
        'Name': "storage",
        'Authors': [
            'Ivan Nikolsky (enty8080) - command developer'
        ],
        'Description': "Manage storage variables.",
        'Usage': "storage [global|local] <option> [arguments]",
        'MinArgs': 2,
        'Options': {
            '-l': ['', "List all storage variables."],
            '-v': ['<name>', "Show specified storage variable value."],
            '-s': ['<name> <value>', "Set storage variable value."],
            '-d': ['<name>', "Delete storage variable."]
        }
    }

    def run(self, argc, argv):
        type_of_storage = argv[1]

        if type_of_storage == "global":
            choice = argv[2]
            if choice in ['-l', '--list']:
                self.print_information("Global storage variables:")
                for variable in self.global_storage.get_all():
                    if not str.startswith(variable, '__') and not str.endswith(variable, '__'):
                        self.print_empty("    * " + variable)
            elif choice in ['-v', '--value']:
                if argv[3] in self.global_storage.get_all():
                    self.print_information(argv[3] + " = " + str(
                        self.global_storage.get(argv[3])))
            elif choice in ['-s', '--set']:
                self.global_storage.set(argv[3], argv[4])
            elif choice in ['-d', '--delete']:
                if argv[3] in self.global_storage.get_all():
                    self.global_storage.delete(argv[3])
                else:
                    self.print_error("Invalid storage variable name!")
        elif type_of_storage == "local":
            choice = argv[2]
            if choice in ['-l', '--list']:
                self.print_information("Local storage variables:")
                for variable in self.local_storage.get_all():
                    if not str.startswith(variable, '__') and not str.endswith(variable, '__'):
                        self.print_empty("    * " + variable)
            elif choice in ['-v', '--value']:
                if argv[3] in self.local_storage.get_all():
                    self.print_information(argv[3] + " = " + str(
                        self.local_storage.get(argv[3])))
                else:
                    self.print_error("Invalid storage variable name!")
            elif choice in ['-s', '--set']:
                self.local_storage.set(argv[3], argv[4])
            elif choice in ['-d', '--delete']:
                if argv[3] in self.local_storage.get_all():
                    self.local_storage.delete(argv[3])
                else:
                    self.print_error("Invalid storage variable name!")
