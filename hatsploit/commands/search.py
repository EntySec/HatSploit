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
    usage += "search [options] <keyword>\n\n"
    usage += "  -w, --where [payloads|modules|plugins]  Select where search.\n"

    details = {
        'Category': "core",
        'Name': "search",
        'Authors': [
            'Ivan Nikolsky (enty8080)'
        ],
        'Description': "Search payloads, modules and plugins.",
        'Usage': usage,
        'MinArgs': 1
    }

    def show_plugins(self, keyword):
        all_plugins = self.local_storage.get("plugins")
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
        modules = self.local_storage.get("modules")
        headers = ("Number", "Module", "Risk", "Description")
        for database in modules.keys():
            number = 0
            modules_data = list()
            for information in modules[database].keys():
                for platform in sorted(modules[database][information].keys()):
                    for module in sorted(modules[database][information][platform].keys()):
                        current_module = modules[database][information][platform]
                        if keyword in information + '/' + platform + '/' + module or keyword in current_module[module]['Description']:
                            name = current_module[module]['Module'].replace(keyword, self.RED + keyword + self.END)
                            description = current_module[module]['Description'].replace(keyword, self.RED + keyword + self.END)

                            modules_data.append((number, name, current_module[module]['Risk'],
                                                description))
                            number += 1
            if modules_data:
                self.print_table("Modules (" + database + ")", headers, *modules_data)

    def show_payloads(self, keyword):
        payloads = self.local_storage.get("payloads")
        headers = ("Number", "Category", "Payload", "Risk", "Description")

        for database in sorted(payloads.keys()):
            number = 0
            payloads_data = list()
            for platform in sorted(payloads[database].keys()):
                for architecture in sorted(payloads[database][platform].keys()):
                    for payload in sorted(payloads[database][platform][architecture].keys()):
                        current_payload = payloads[database][platform][architecture][payload]
                        if keyword in platform + '/' + architecture + '/' + payload or keyword in current_payload['Description']:
                            name = current_payload['Payload'].replace(keyword, self.RED + keyword + self.END)
                            description = current_payload['Description'].replace(keyword, self.RED + keyword + self.END)

                            payloads_data.append((number, current_payload['Category'], name,
                                                current_payload['Risk'], description))
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
