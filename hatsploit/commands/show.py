#!/usr/bin/env python3

#
# This command requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.lib.command import Command
from hatsploit.lib.show import Show
from hatsploit.lib.storage import LocalStorage


class HatSploitCommand(Command):
    local_storage = LocalStorage()
    show = Show()

    details = {
        'Category': "core",
        'Name': "show",
        'Authors': [
            'Ivan Nikolsky (enty8080) - command developer'
        ],
        'Description': "Show specified information.",
        'Usage': self.usage(),
        'MinArgs': 1
    }

    def print_usage(self):
        options = self.modules.check_current_module()
        payloads = self.local_storage.get("payloads")
        modules = self.local_storage.get("modules")
        plugins = self.local_storage.get("plugins")

        informations = list()
        if modules:
            for database in sorted(modules.keys()):
                for module in sorted(modules[database].keys()):
                    info = module.split('/')[0]
                    if info not in informations:
                        informations.append(info)

        if informations or plugins or options:
            usage = "show ["

            if payloads:
                usage += "payloads|"
            for information in informations:
                usage += information + "|"
            if plugins:
                usage += "plugins|"
            if options:
                usage += "options"
            else:
                usage = usage[:-2] + "]"
            return usage
        else:
            return "show []"

    def run(self, argc, argv):
        information = argv[1]

        options = self.modules.check_current_module()
        payloads = self.local_storage.get("payloads")
        modules = self.local_storage.get("modules")
        plugins = self.local_storage.get("plugins")

        informations = list()
        if modules:
            for database in sorted(modules.keys()):
                for module in sorted(modules[database].keys()):
                    info = module.split('/')[0]
                    if info not in informations:
                        informations.append(info)

        if payloads:
            if information == "payloads":
                self.show.show_payloads()
                return
        if plugins:
            if information == "plugins":
                self.show.show_plugins()
                return
        if options:
            if information == "options":
                self.show.show_options()
                return
        if information in informations:
            self.show.show_modules(information)
        else:
            self.print_usage(self.details['Usage'])
