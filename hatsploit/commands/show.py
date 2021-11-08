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
    else:
        usage = "show []"

    details = {
        'Category': "core",
        'Name': "show",
        'Authors': [
            'Ivan Nikolsky (enty8080) - command developer'
        ],
        'Description': "Show specified information.",
        'Usage': usage,
        'MinArgs': 1
    }

    def run(self, argc, argv):
        if self.payloads:
            if information == "payloads":
                self.show.show_payloads()
                return
        if self.plugins:
            if information == "plugins":
                self.show.show_plugins()
                return
        if self.options:
            if information == "options":
                self.show.show_options()
                return
        if information in self.informations:
            self.show.show_modules(information)
        else:
            self.print_usage(self.details['Usage'])
