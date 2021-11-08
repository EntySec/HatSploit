#!/usr/bin/env python3

#
# This command requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.lib.command import Command
from hatsploit.lib.show import Show
from hatsploit.lib.modules import Modules
from hatsploit.lib.storage import LocalStorage


class HatSploitCommand(Command):
    local_storage = LocalStorage()
    show = Show()
    modules = Modules()

    details = {
        'Category': "core",
        'Name': "show",
        'Authors': [
            'Ivan Nikolsky (enty8080) - command developer'
        ],
        'Description': "Show specified information.",
        'Usage': "show <information>",
        'MinArgs': 1
    }

    def usage(self):
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

        if informations or plugins or options or payloads:
            usage = "show ["

            if payloads:
                usage += "payloads|"
            for information in informations:
                usage += information + "|"
            if plugins:
                usage += "plugins|"
            if options:
                usage += "options]"
            else:
                usage = usage[:-1] + "]"
        else:
            usage = "show []"

        return usage

    def run(self, argc, argv):
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
            if argv[1] == "payloads":
                self.show.show_payloads()
                return
        if plugins:
            if argv[1] == "plugins":
                self.show.show_plugins()
                return
        if options:
            if argv[1] == "options":
                self.show.show_options()
                return
        if argv[1] in informations:
            self.show.show_modules(argv[1])
        else:
            self.print_usage(self.usage())
