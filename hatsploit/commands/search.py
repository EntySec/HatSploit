#!/usr/bin/env python3

#
# This command requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.lib.command import Command
from hatsploit.lib.storage import LocalStorage


class HatSploitCommand(Command):
    local_storage = LocalStorage()

    usage = ""
    usage += "search [option] [<keyword>]\n\n"
    usage += "  -w, --where [payloads|modules|plugins]  Select where search.\n"

    details = {
        'Category': "core",
        'Name': "search",
        'Authors': [
            'Ivan Nikolsky (enty8080) - command developer'
        ],
        'Description': "Search payloads, modules and plugins.",
        'Usage': usage,
        'MinArgs': 1
    }

    def show_plugins(self, keyword):
        all_plugins = self.local_storage.get("plugins")
        if all_plugins:
            headers = ("Number", "Name", "Description")
            for database in all_plugins.keys():
                number = 0
                plugins_data = list()
                plugins = all_plugins[database]
                for plugin in sorted(plugins.keys()):
                    if keyword in plugin or keyword in plugins[plugin]['Description']:
                        name = plugin.replace(keyword, self.RED + keyword + self.END)
                        description = plugins[plugin]['Description'].replace(keyword, self.RED + keyword + self.END)

                        plugins_data.append((number, name, description))
                        number += 1
                if plugins_data:
                    self.print_table("Plugins (" + database + ")", headers, *plugins_data)

    def show_modules(self, keyword):
        all_modules = self.local_storage.get("modules")
        if all_modules:
            headers = ("Number", "Module", "Risk", "Description")
            for database in all_modules.keys():
                number = 0
                modules_data = list()
                modules = all_modules[database]
                for module in sorted(modules.keys()):
                    if keyword in module or keyword in modules[module]['Description']:
                        name = module.replace(keyword, self.RED + keyword + self.END)
                        description = modules[module]['Description'].replace(keyword, self.RED + keyword + self.END)

                        modules_data.append((number, name, modules[module]['Risk'], description))
                        number += 1
                if modules_data:
                    self.print_table("Modules (" + database + ")", headers, *modules_data)

    def show_payloads(self, keyword):
        all_payloads = self.local_storage.get("payloads")
        if all_payloads:
            headers = ("Number", "Category", "Payload", "Risk", "Description")
            for database in all_payloads.keys():
                number = 0
                payloads_data = list()
                payloads = all_payloads[database]
                for payload in sorted(payloads.keys()):
                    if keyword in payload or keyword in payloads[payload]['Description']:
                        name = payload.replace(keyword, self.RED + keyword + self.END)
                        description = payloads[payload]['Description'].replace(keyword, self.RED + keyword + self.END)

                        payloads_data.append((number, payloads[payload]['Category'], name,
                                              payloads[payload]['Risk'], description))
                        number += 1
                if payloads_data:
                    self.print_table("Payloads (" + database + ")", headers, *payloads_data)

    def run(self, argc, argv):
        if argv[0] not in ['-w', '--where']:
            self.show_modules(argv[0])
            self.show_payloads(argv[0])
            self.show_plugins(argv[0])
        else:
            if argc < 3:
                self.output_usage(self.details['Usage'])
            else:
                if argv[1] == 'modules':
                    self.show_modules(argv[2])
                elif argv[1] == 'payloads':
                    self.show_payloads(argv[2])
                elif argv[1] == 'plugins':
                    self.show_plugins(argv[2])
                else:
                    self.output_usage(self.details['Usage'])
