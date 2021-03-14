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

from core.lib.command import HatSploitCommand

from core.base.storage import local_storage
from core.modules.modules import modules
from core.payloads.payloads import payloads

class HatSploitCommand(HatSploitCommand):
    local_storage = local_storage()
    modules = modules()
    payloads = payloads()

    details = {
        'Category': "core",
        'Name': "show",
        'Authors': [
            'enty8080'
        ],
        'Description': "Show specified information.",
        'Usage': "show <information>",
        'MinArgs': 1
    }

    def show_plugins(self):
        plugins = self.local_storage.get("plugins")
        plugins_data = list()
        number = 0
        headers = ("Number", "Name", "Database", "Description")
        for database in plugins.keys():
            plugins = plugins[database]
            for plugin in sorted(plugins.keys()):
                plugins_data.append((number, plugin, database, plugins[plugin]['Description']))
                number += 1
        self.tables.print_table("Plugins", headers, *plugins_data)

    def show_modules(self, information):
        modules = self.local_storage.get("modules")
        modules_data = list()
        number = 0
        headers = ("Number", "Module", "Database", "Risk", "Description")
        for database in modules.keys():
            modules = modules[database][information]
            for platform in sorted(modules.keys()):
                for module in sorted(modules[platform].keys()):
                    full_name = self.modules.get_full_name(information, platform, module)
                    modules_data.append((number, full_name, database, modules[platform][module]['Risk'], modules[platform][module]['Description']))
                    number += 1
        self.tables.print_table(information.title() + " Modules", headers, *modules_data)

    def show_payloads(self):
        payloads_data = dict()
        payloads = self.local_storage.get("payloads")
        headers = ("Number", "Payload", "Database", "Risk", "Description")
        number = 0

        for database in sorted(payloads.keys()):
            for platform in sorted(payloads[database].keys()):
                for architecture in sorted(payloads[database][platform].keys()):
                    payloads = payloads[database][platform][architecture]
                    for payload in sorted(payloads.keys()):
                        label = payloads[payload]['Category']
                        payloads_data[label] = list()
                    for payload in sorted(payloads.keys()):
                        label = payloads[payload]['Category']
                        payloads_data[label].append((number, payload, database, payloads[payload]['Risk'], payloads[payload]['Description']))
                        number += 1
                    for label in sorted(payloads_data.keys()):
                        self.tables.print_table("Payloads (" + label + ")", headers, *payloads_data[label])

    def show_options(self):
        current_module = self.modules.get_current_module_object()
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
        self.tables.print_table("Module Options (" + current_module.details['Module'] + ")", headers, *options_data)

        options_data = list()
        for option in sorted(options.keys()):
            if options[option]['Type'] and options[option]['Type'].lower() == 'payload':
                current_payload = self.payloads.get_current_payload()
                if current_payload:
                    for option in sorted(current_payload.options.keys()):
                        value, required = current_payload.options[option]['Value'], current_payload.options[option]['Required']
                        if required:
                            required = "yes"
                        else:
                            required = "no"
                        if not value and value != 0:
                            value = ""
                        options_data.append((option, value, required, current_payload.options[option]['Description']))
                    self.tables.print_table("Payload Options (" + current_payload.details['Payload'] + ")", headers, *options_data)

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
            self.badges.output_information(usage)
        else:
            self.badges.output_warning("No informations available!")

    def run(self, argc, argv):
        information = argv[0]

        if self.modules.check_current_module():
            current_module = self.modules.get_current_module_object()

            options = False
            if hasattr(current_module, "options"):
                options = True
        else:
            options = False

        payloads = self.local_storage.get("payloads")
        modules = self.local_storage.get("modules")
        plugins = self.local_storage.get("plugins")

        informations = list()
        if modules:
            for database in sorted(modules.keys()):
                for category in sorted(modules[database].keys()):
                    informations.append(category)

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
