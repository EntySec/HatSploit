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

from hatsploit.lib.jobs import Jobs
from hatsploit.lib.storage import LocalStorage
from hatsploit.lib.modules import Modules
from hatsploit.lib.payloads import Payloads

from hatsploit.core.cli.colors import Colors
from hatsploit.core.cli.badges import Badges
from hatsploit.core.cli.tables import Tables


class Show:
    jobs = Jobs()
    local_storage = LocalStorage()
    modules = Modules()
    payloads = Payloads()

    colors = Colors()
    badges = Badges()
    tables = Tables()

    def show_custom_commands(self, handler):
        commands_data = dict()
        headers = ("Command", "Description")
        commands = handler

        for command in sorted(commands.keys()):
            label = commands[command].details['Category']
            commands_data[label] = list()
        for command in sorted(commands.keys()):
            label = commands[command].details['Category']
            commands_data[label].append((command, commands[command].details['Description']))
        for label in sorted(commands_data.keys()):
            self.tables.print_table(label.title() + " Commands", headers, *commands_data[label])

    def show_interface_commands(self):
        if self.local_storage.get("commands"):
            self.show_custom_commands(self.local_storage.get("commands"))
        else:
            self.badges.print_warning("No commands available.")

    def show_plugin_commands(self):
        for plugin in self.local_storage.get("loaded_plugins").keys():
            loaded_plugin = self.local_storage.get("loaded_plugins")[plugin]
            if hasattr(loaded_plugin, "commands"):
                commands_data = dict()
                headers = ("Command", "Description")
                commands = loaded_plugin.commands
                for label in sorted(commands.keys()):
                    commands_data[label] = list()
                    for command in sorted(commands[label].keys()):
                        commands_data[label].append((command, commands[label][command]['Description']))
                for label in sorted(commands_data.keys()):
                    self.tables.print_table(label.title() + " Commands", headers, *commands_data[label])

    def show_module_commands(self):
        current_module = self.modules.get_current_module_object()
        if hasattr(current_module, "commands"):
            commands_data = list()
            headers = ("Command", "Description")
            commands = current_module.commands
            for command in sorted(commands.keys()):
                commands_data.append((command, commands[command]['Description']))
            self.tables.print_table("Module Commands", headers, *commands_data)

    def show_all_commands(self):
        self.show_interface_commands()
        if self.modules.check_current_module():
            self.show_module_commands()
        if self.local_storage.get("loaded_plugins"):
            self.show_plugin_commands()

    def show_jobs(self):
        if self.local_storage.get("jobs"):
            jobs_data = list()
            headers = ("ID", "Name", "Module")
            jobs = self.local_storage.get("jobs")
            for job_id in jobs.keys():
                jobs_data.append((job_id, jobs[job_id]['job_name'], jobs[job_id]['module_name']))
            self.tables.print_table("Active Jobs", headers, *jobs_data)
        else:
            self.badges.print_warning("No running jobs available.")

    def show_module_databases(self):
        if self.local_storage.get("connected_modules_databases"):
            databases_data = list()
            number = 0
            headers = ("Number", "Name", "Path")
            databases = self.local_storage.get("connected_modules_databases")
            for name in databases.keys():
                databases_data.append((number, name, databases[name]['path']))
                number += 1
            self.tables.print_table("Connected Module Databases", headers, *databases_data)
        else:
            self.badges.print_warning("No module database connected.")

    def show_payload_databases(self):
        if self.local_storage.get("connected_payloads_databases"):
            databases_data = list()
            number = 0
            headers = ("Number", "Name", "Path")
            databases = self.local_storage.get("connected_payload_databases")
            for name in databases.keys():
                databases_data.append((number, name, databases[name]['path']))
                number += 1
            self.tables.print_table("Connected Payload Databases", headers, *databases_data)
        else:
            self.badges.print_warning("No payload database connected.")

    def show_plugin_databases(self):
        if self.local_storage.get("connected_plugins_databases"):
            databases_data = list()
            number = 0
            headers = ("Number", "Name", "Path")
            databases = self.local_storage.get("connected_plugins_databases")
            for name in databases.keys():
                databases_data.append((number, name, databases[name]['path']))
                number += 1
            self.tables.print_table("Connected Plugin Databases", headers, *databases_data)
        else:
            self.badges.print_warning("No plugin database connected.")

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
            self.tables.print_table("Plugins (" + database + ")", headers, *plugins_data)

    def show_modules(self, information):
        all_modules = self.local_storage.get("modules")
        headers = ("Number", "Module", "Rank", "Description")
        for database in sorted(all_modules.keys()):
            number = 0
            modules_data = list()
            modules = all_modules[database]
            for module in sorted(modules.keys()):
                if information == module.split('/')[0]:
                    modules_data.append((number, modules[module]['Module'], modules[module]['Rank'],
                                         modules[module]['Description']))
                    number += 1
            self.tables.print_table(information.title() + " Modules (" + database + ")", headers, *modules_data)

    def show_payloads(self):
        all_payloads = self.local_storage.get("payloads")
        headers = ("Number", "Category", "Payload", "Rank", "Description")
        for database in sorted(all_payloads.keys()):
            number = 0
            payloads_data = list()
            payloads = all_payloads[database]
            for payload in sorted(payloads.keys()):
                payloads_data.append((number, payloads[payload]['Category'], payloads[payload]['Payload'],
                                      payloads[payload]['Rank'], payloads[payload]['Description']))
                number += 1
            self.tables.print_table("Payloads (" + database + ")", headers, *payloads_data)

    def show_search_plugins(self, keyword):
        all_plugins = self.local_storage.get("plugins")
        if all_plugins:
            headers = ("Number", "Name", "Description")
            for database in all_plugins.keys():
                number = 0
                plugins_data = list()
                plugins = all_plugins[database]
                for plugin in sorted(plugins.keys()):
                    if keyword in plugin or keyword in plugins[plugin]['Description']:
                        name = plugin.replace(keyword, self.colors.RED + keyword + self.colors.END)
                        description = plugins[plugin]['Description'].replace(keyword, self.colors.RED + keyword + self.colors.END)

                        plugins_data.append((number, name, description))
                        number += 1
                if plugins_data:
                    self.tables.print_table("Plugins (" + database + ")", headers, *plugins_data)

    def show_search_modules(self, keyword):
        all_modules = self.local_storage.get("modules")
        if all_modules:
            headers = ("Number", "Module", "Rank", "Description")
            for database in all_modules.keys():
                number = 0
                modules_data = list()
                modules = all_modules[database]
                for module in sorted(modules.keys()):
                    if keyword in module or keyword in modules[module]['Description']:
                        name = module.replace(keyword, self.colors.RED + keyword + self.colors.END)
                        description = modules[module]['Description'].replace(keyword, self.colors.RED + keyword + self.colors.END)

                        modules_data.append((number, name, modules[module]['Rank'], description))
                        number += 1
                if modules_data:
                    self.tables.print_table("Modules (" + database + ")", headers, *modules_data)

    def search_show_payloads(self, keyword):
        all_payloads = self.local_storage.get("payloads")
        if all_payloads:
            headers = ("Number", "Category", "Payload", "Rank", "Description")
            for database in all_payloads.keys():
                number = 0
                payloads_data = list()
                payloads = all_payloads[database]
                for payload in sorted(payloads.keys()):
                    if keyword in payload or keyword in payloads[payload]['Description']:
                        name = payload.replace(keyword, self.colors.RED + keyword + self.colors.END)
                        description = payloads[payload]['Description'].replace(keyword, self.colors.RED + keyword + self.colors.END)

                        payloads_data.append((number, payloads[payload]['Category'], name,
                                              payloads[payload]['Rank'], description))
                        number += 1
                if payloads_data:
                    self.tables.print_table("Payloads (" + database + ")", headers, *payloads_data)

    def show_module_information(self, current_module):
        authors = ""
        for author in current_module['Authors']:
            authors += author + ", "
        authors = authors[:-2]

        comments = ""
        for line in current_module['Comments']:
            comments += line + "\n" + (" " * 14)
        comments = comments[:-15]

        self.badges.print_information("Module information:")
        self.badges.print_empty("")

        if current_module['Name']:
            self.badges.print_empty("         Name: " + current_module['Name'])
        if current_module['Module']:
            self.badges.print_empty("       Module: " + current_module['Module'])
        if authors:
            self.badges.print_empty("      Authors: ")
            for author in current_module['Authors']:
                self.badges.print_empty("               " + author)
        if current_module['Description']:
            self.badges.print_empty("  Description: " + current_module['Description'])
        if comments:
            self.badges.print_empty("     Comments: ")
            self.badges.print_empty("               " + comments)
        if current_module['Rank']:
            self.badges.print_empty("         Rank: " + current_module['Rank'])

        self.badges.print_empty("")

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
            self.tables.print_table("Module Options (" + current_module.details['Module'] + ")", headers, *options_data)

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
                    self.tables.print_table("Payload Options (" + current_payload.details['Payload'] + ")", headers,
                                     *options_data)
