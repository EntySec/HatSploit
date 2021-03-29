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

from core.lib.command import Command
from core.base.storage import LocalStorage


class HatSploitCommand(Command):
    local_storage = LocalStorage()

    details = {
        'Category': "core",
        'Name': "search",
        'Authors': [
            'enty8080'
        ],
        'Description': "Search payloads, modules and plugins.",
        'Usage': "search <keyword>",
        'MinArgs': 1
    }

    def show_plugins(self, keyword):
        plugins = self.local_storage.get("plugins")
        headers = ("Number", "Name", "Description")
        for database in plugins.keys():
            number = 0
            plugins_data = list()
            plugins = plugins[database]
            for plugin in sorted(plugins.keys()):
                if keyword in plugin:
                    name = plugin.replace(keyword, self.RED + keyword + self.END)
                    plugins_data.append((number, name, plugins[plugin]['Description']))
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
                    for module in sorted(modules[database][infotmation][platform].keys()):
                        if keyword in information + '/' + platform + '/' + module:
                            current_module = modules[database][information][platform]
                            name = current_module[module]['Module'].replace(keyword, self.RED + keyword + self.END)
                            modules_data.append((number, name, current_module[module]['Risk'],
                                                current_module[module]['Description']))
                            number += 1
            if modules_data:
                self.print_table(" Modules (" + database + ")", headers, *modules_data)

    def show_payloads(self, keyword):
        payloads = self.local_storage.get("payloads")
        headers = ("Number", "Category", "Payload", "Risk", "Description")

        for database in sorted(payloads.keys()):
            number = 0
            payloads_data = list()
            for platform in sorted(payloads[database].keys()):
                for architecture in sorted(payloads[database][platform].keys()):
                    for payload in sorted(payloads[database][platform][architecture].keys()):
                        if keyword in platform + '/' + architecture + '/' + payload:
                            current_payload = payloads[database][platform][architecture][payload]
                            name = current_payload['Payload'].replace(keyword, self.RED + keyword + self.END)
                            payloads_data.append((number, current_payload['Category'], name,
                                                current_payload['Risk'], current_payload['Description']))
                            number += 1
            if payloads_data:
                self.print_table("Payloads (" + database + ")", headers, *payloads_data)

    def run(self, argc, argv):
        keyword = argv[0]

        self.show_payloads(keyword)
        self.show_modules(keyword)
        self.show_plugins(keyword)
