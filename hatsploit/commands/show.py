#!/usr/bin/env python3

#
# This command requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.lib.storage import LocalStorage
from hatsploit.lib.command import Command
from hatsploit.lib.modules import Modules
from hatsploit.lib.payloads import Payloads


class HatSploitCommand(Command):
    local_storage = LocalStorage()
    modules = Modules()
    payloads = Payloads()

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

    def show_plugins(self):
        all_plugins = self.local_storage.get("plugins")
        headers = ("Number", "Name", "Description")
        for database in sorted(all_plugins.keys()):
            number = 0
            plugins_data = list()
            plugins = all_plugins[database]
            for plugin in sorted(plugins.keys()):
                plugins_data.append((number, plugin, plugins[plugin]['Description']))
                number += 1
            self.print_table("Plugins (" + database + ")", headers, *plugins_data)

    def show_modules(self, information):
        all_modules = self.local_storage.get("modules")
        headers = ("Number", "Module", "Risk", "Description")
        for database in sorted(all_modules.keys()):
            number = 0
            modules_data = list()
            modules = all_modules[database]
            for module in sorted(modules.keys()):
                if information == module.split('/')[0]:
                    modules_data.append((number, modules[module]['Module'], modules[module]['Risk'],
                                         modules[module]['Description']))
                    number += 1
            self.print_table(information.title() + " Modules (" + database + ")", headers, *modules_data)

    def show_payloads(self):
        all_payloads = self.local_storage.get("payloads")
        headers = ("Number", "Category", "Payload", "Risk", "Description")
        for database in sorted(all_payloads.keys()):
            number = 0
            payloads_data = list()
            payloads = all_payloads[database]
            for payload in sorted(payloads.keys()):
                payloads_data.append((number, payloads[payload]['Category'], payloads[payload]['Payload'],
                                      payloads[payload]['Risk'], payloads[payload]['Description']))
                number += 1
            self.print_table("Payloads (" + database + ")", headers, *payloads_data)

    def show_options(self):
        current_module = self.modules.get_current_module_object()

        if not hasattr(current_module, "options") and not hasattr(current_module, "payload"):
            self.badges.print_warning("Module has no options.")
            return

        if not hasattr(current_module, "options") and not hasattr(self.payloads.get_current_payload(), "options"):
            self.badges.print_warning("Module has no options.")
            return

        if hasattr(current_module, "options"):
            options_data = list()
            headers = ("Option", "Value", "Required", "Description")
            options = current_module.options

            for option in sorted(options.keys()):
                value, required = options[option]['Value'], options[option]['Required']
                if required:
                    required = "yes"
                else:
                    required = "no"
                if not value and value != 0:
                    value = ""
                options_data.append((option, value, required, options[option]['Description']))
            self.print_table("Module Options (" + current_module.details['Module'] + ")", headers, *options_data)

        if hasattr(current_module, "payload"):
            if hasattr(self.payloads.get_current_payload(), "options"):
                options_data = list()
                headers = ("Option", "Value", "Required", "Description")
                current_payload = self.payloads.get_current_payload()
                if current_payload:
                    for option in sorted(current_payload.options.keys()):
                        value, required = current_payload.options[option]['Value'], \
                                        current_payload.options[option]['Required']
                        if required:
                            required = "yes"
                        else:
                            required = "no"
                        if not value and value != 0:
                            value = ""
                        options_data.append((option, value, required, current_payload.options[option]['Description']))
                    self.print_table("Payload Options (" + current_payload.details['Payload'] + ")", headers, *options_data)

    def print_usage(self, informations, plugins, options):
        if informations or plugins or options:
            usage = "Informations: "
            if self.local_storage.get("payloads"):
                usage += "payloads, "
            for information in informations:
                usage += information + ", "
            if plugins:
                usage += "plugins, "
            if options:
                usage += "options"
            else:
                usage = usage[:-2]
            self.print_information(usage)
        else:
            self.print_warning("No informations available!")

    def run(self, argc, argv):
        information = argv[0]

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
                self.show_payloads()
                return
        if plugins:
            if information == "plugins":
                self.show_plugins()
                return
        if options:
            if information == "options":
                self.show_options()
                return
        if information in informations:
            self.show_modules(information)
        else:
            self.print_usage(informations, plugins, options)
