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
            'Ivan Nikolsky (enty8080) - command developer'
        ],
        'Description': "Manage storage variables.",
        'Usage': usage,
        'MinArgs': 2
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
                if argc < 4:
                    self.print_usage(self.details['Usage'])
                else:
                    if argv[3] in self.global_storage.get_all():
                        self.print_information(argv[3] + " = " + str(
                            self.global_storage.get(argv[3])))
            elif choice in ['-s', '--set']:
                if argc < 5:
                    self.print_usage(self.details['Usage'])
                else:
                    self.global_storage.set(argv[3], argv[4])
            elif choice in ['-d', '--delete']:
                if argc < 4:
                    self.print_usage(self.details['Usage'])
                else:
                    if argv[3] in self.global_storage.get_all():
                        self.global_storage.delete(argv[3])
                    else:
                        self.print_error("Invalid storage variable name!")
            else:
                self.print_usage(self.details['Usage'])
        elif type_of_storage == "local":
            choice = argv[2]
            if choice in ['-l', '--list']:
                self.print_information("Local storage variables:")
                for variable in self.local_storage.get_all():
                    if not str.startswith(variable, '__') and not str.endswith(variable, '__'):
                        self.print_empty("    * " + variable)
            elif choice in ['-v', '--value']:
                if argc < 4:
                    self.print_usage(self.details['Usage'])
                else:
                    if argv[3] in self.local_storage.get_all():
                        self.print_information(argv[3] + " = " + str(
                            self.local_storage.get(argv[3])))
                    else:
                        self.print_error("Invalid storage variable name!")
            elif choice in ['-s', '--set']:
                if argc < 5:
                    self.print_usage(self.details['Usage'])
                else:
                    self.local_storage.set(argv[3], argv[4])
            elif choice in ['-d', '--delete']:
                if argc < 4:
                    self.print_usage(self.details['Usage'])
                else:
                    if argv[3] in self.local_storage.get_all():
                        self.local_storage.delete(argv[3])
                    else:
                        self.print_error("Invalid storage variable name!")
            else:
                self.print_usage(self.details['Usage'])
        else:
            self.print_usage(self.details['Usage'])
