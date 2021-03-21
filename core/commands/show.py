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

from core.base.storage import LocalStorage
from core.lib.command import Command
from core.modules.modules import Modules
from core.payloads.payloads import Payloads


class HatSploitCommand(Command):
    local_storage = LocalStorage()
    modules = Modules()
    payloads = Payloads()

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
        headers = ("Number", "Name", "Description")
        for database in plugins.keys():
            number = 0
            plugins_data = list()
            plugins = plugins[database]
            for plugin in sorted(plugins.keys()):
                plugins_data.append((number, plugin, plugins[plugin]['Description']))
                number += 1
            self.print_table("Plugins (" + database + ")", headers, *plugins_data)

    def show_modules(self, information):
        modules = self.local_storage.get("modules")
        headers = ("Number", "Module", "Risk", "Description")
        for database in modules.keys():
            number = 0
            modules_data = list()
            modules = modules[database][information]
            for platform in sorted(modules.keys()):
                for module in sorted(modules[platform].keys()):
                    modules_data.append((number, modules[platform][module]['Module'], modules[platform][module]['Risk'],
                                         modules[platform][module]['Description']))
                    number += 1
            self.print_table(information.title() + " Modules (" + database + ")", headers, *modules_data)

    def show_payloads(self):
        payloads = self.local_storage.get("payloads")
        headers = ("Number", "Category", "Payload", "Risk", "Description")

        for database in sorted(payloads.keys()):
            number = 0
            payloads_data = list()
            for platform in sorted(payloads[database].keys()):
                for architecture in sorted(payloads[database][platform].keys()):
                    for payload in sorted(payloads[database][platform][architecture].keys()):
                        current_payload = payloads[database][platform][architecture][payload]
                        payloads_data.append((number, current_payload['Category'], current_payload['Payload'],
                                              current_payload['Risk'], current_payload['Description']))
                        number += 1
            self.print_table("Payloads (" + database + ")", headers, *payloads_data)

    def show_options(self):
        current_module = self.modules.get_current_module_object()

        if not hasattr(current_module, "options") and not hasattr(current_module, "payload"):
            self.badges.output_warning("Module has no options.")
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
            if hasattr(current_module, "payload"):
                payload = current_module.payload
                options_data.append(('PAYLOAD', payload['Value'], "yes", payload['Description']))
            self.print_table("Module Options (" + current_module.details['Module'] + ")", headers, *options_data)

        if hasattr(current_module, "payload"):
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
            self.output_information(usage)
        else:
            self.output_warning("No informations available!")

    def run(self, argc, argv):
        information = argv[0]

        if self.modules.check_current_module():
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
