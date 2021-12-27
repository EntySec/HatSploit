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
from hatsploit.lib.loot import Loot
from hatsploit.lib.storage import LocalStorage
from hatsploit.lib.modules import Modules
from hatsploit.lib.payloads import Payloads
from hatsploit.lib.sessions import Sessions

from hatsploit.core.cli.colors import Colors
from hatsploit.core.cli.badges import Badges
from hatsploit.core.cli.tables import Tables


class Show:
    jobs = Jobs()
    loot = Loot()
    local_storage = LocalStorage()
    modules = Modules()
    payloads = Payloads()
    sessions = Sessions()

    colors = Colors()
    badges = Badges()
    tables = Tables()

    def show_custom_commands(self, handler):
        commands_data = {}
        headers = ("Command", "Description")
        commands = handler

        for command in sorted(commands):
            label = commands[command].details['Category']
            commands_data[label] = []
        for command in sorted(commands):
            label = commands[command].details['Category']
            commands_data[label].append((command, commands[command].details['Description']))
        for label in sorted(commands_data):
            self.tables.print_table(label.title() + " Commands", headers, *commands_data[label])

    def show_interface_commands(self):
        if self.local_storage.get("commands"):
            self.show_custom_commands(self.local_storage.get("commands"))
        else:
            self.badges.print_warning("No commands available.")

    def show_plugin_commands(self):
        for plugin in self.local_storage.get("loaded_plugins"):
            loaded_plugin = self.local_storage.get("loaded_plugins")[plugin]
            if hasattr(loaded_plugin, "commands"):
                commands_data = {}
                headers = ("Command", "Description")
                commands = loaded_plugin.commands
                for label in sorted(commands):
                    commands_data[label] = []
                    for command in sorted(commands[label]):
                        commands_data[label].append((command, commands[label][command]['Description']))
                for label in sorted(commands_data):
                    self.tables.print_table(label.title() + " Commands", headers, *commands_data[label])

    def show_module_commands(self):
        current_module = self.modules.get_current_module_object()
        if hasattr(current_module, "commands"):
            commands_data = []
            headers = ("Command", "Description")
            commands = current_module.commands
            for command in sorted(commands):
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
            jobs_data = []
            headers = ("ID", "Name", "Module")
            jobs = self.local_storage.get("jobs")
            for job_id in jobs:
                jobs_data.append((job_id, jobs[job_id]['job_name'], jobs[job_id]['module_name']))
            self.tables.print_table("Active Jobs", headers, *jobs_data)
        else:
            self.badges.print_warning("No running jobs available.")

    def show_loot(self):
        loots = self.loot.list_loot()
        if loots:
            headers = ("Loot", "Path", "Time")
            self.tables.print_table("Collected Loot", headers, *loots)
        else:
            self.badges.print_warning("No loot collected yet.")

    def show_module_databases(self):
        if self.local_storage.get("connected_module_databases"):
            databases_data = []
            number = 0
            headers = ("Number", "Name", "Path")
            databases = self.local_storage.get("connected_module_databases")

            for name in databases:
                databases_data.append((number, name, databases[name]['path']))
                number += 1
            self.tables.print_table("Connected Module Databases", headers, *databases_data)
        else:
            self.badges.print_warning("No module database connected.")

    def show_payload_databases(self):
        if self.local_storage.get("connected_payload_databases"):
            databases_data = []
            number = 0
            headers = ("Number", "Name", "Path")
            databases = self.local_storage.get("connected_payload_databases")

            for name in databases:
                databases_data.append((number, name, databases[name]['path']))
                number += 1
            self.tables.print_table("Connected Payload Databases", headers, *databases_data)
        else:
            self.badges.print_warning("No payload database connected.")

    def show_plugin_databases(self):
        if self.local_storage.get("connected_plugin_databases"):
            databases_data = []
            number = 0
            headers = ("Number", "Name", "Path")
            databases = self.local_storage.get("connected_plugin_databases")

            for name in databases:
                databases_data.append((number, name, databases[name]['path']))
                number += 1
            self.tables.print_table("Connected Plugin Databases", headers, *databases_data)
        else:
            self.badges.print_warning("No plugin database connected.")

    def show_plugins(self):
        all_plugins = self.local_storage.get("plugins")
        headers = ("Number", "Name", "Description")
        plugins_shorts = {}

        for database in sorted(all_plugins):
            number = 0
            plugins_data = []
            plugins = all_plugins[database]

            for plugin in sorted(plugins):
                plugins_data.append((number, plugin, plugins[plugin]['Description']))
                plugins_shorts.update({number: plugin})
                number += 1

            self.tables.print_table(f"Plugins ({database})", headers, *plugins_data)
            self.local_storage.set("plugin_shorts", plugins_shorts)

    def show_modules(self, information):
        all_modules = self.local_storage.get("modules")
        headers = ("Number", "Module", "Rank", "Description")
        modules_shorts = {}

        for database in sorted(all_modules):
            number = 0
            modules_data = []
            modules = all_modules[database]

            for module in sorted(modules):
                if information == module.split('/')[0]:
                    modules_data.append((number, modules[module]['Module'], modules[module]['Rank'],
                                         modules[module]['Description']))
                    modules_shorts.update({number: modules[module]['Module']})
                    number += 1

            self.tables.print_table(f"{information.title()} Modules ({database})", headers, *modules_data)
            self.local_storage.set("module_shorts", modules_shorts)

    def show_payloads(self):
        all_payloads = self.local_storage.get("payloads")
        headers = ("Number", "Category", "Payload", "Rank", "Description")
        payloads_shorts = {}

        for database in sorted(all_payloads):
            number = 0
            payloads_data = []
            payloads = all_payloads[database]

            for payload in sorted(payloads):
                payloads_data.append((number, payloads[payload]['Category'], payloads[payload]['Payload'],
                                      payloads[payload]['Rank'], payloads[payload]['Description']))
                payloads_shorts.update({number: payloads[payload]['Payload']})
                number += 1

            self.tables.print_table(f"Payloads ({database})", headers, *payloads_data)
            self.local_storage.set("payload_shorts", payloads_shorts)

    def show_search_plugins(self, keyword):
        all_plugins = self.local_storage.get("plugins")
        plugins_shorts = {}

        if all_plugins:
            headers = ("Number", "Name", "Description")
            for database in all_plugins:
                number = 0
                plugins_data = []
                plugins = all_plugins[database]

                for plugin in sorted(plugins):
                    if keyword in plugin or keyword in plugins[plugin]['Description']:
                        name = plugin.replace(keyword, self.colors.RED + keyword + self.colors.END)
                        description = plugins[plugin]['Description'].replace(keyword, self.colors.RED + keyword + self.colors.END)

                        plugins_data.append((number, name, description))
                        plugins_shorts.update({number: plugin})

                        number += 1
                if plugins_data:
                    self.tables.print_table(f"Plugins ({database})", headers, *plugins_data)
                    self.local_storage.set("plugin_shorts", plugins_shorts)

    def show_search_modules(self, keyword):
        all_modules = self.local_storage.get("modules")
        modules_shorts = {}

        if all_modules:
            headers = ("Number", "Module", "Rank", "Description")
            for database in all_modules:
                number = 0
                modules_data = []
                modules = all_modules[database]

                for module in sorted(modules):
                    if keyword in module or keyword in modules[module]['Description']:
                        name = module.replace(keyword, self.colors.RED + keyword + self.colors.END)
                        description = modules[module]['Description'].replace(keyword, self.colors.RED + keyword + self.colors.END)

                        modules_data.append((number, name, modules[module]['Rank'], description))
                        modules_shorts.update({number: module})

                        number += 1
                if modules_data:
                    self.tables.print_table(f"Modules ({database})", headers, *modules_data)
                    self.local_storage.set("module_shorts", modules_shorts)

    def show_search_payloads(self, keyword):
        all_payloads = self.local_storage.get("payloads")
        payloads_shorts = {}

        if all_payloads:
            headers = ("Number", "Category", "Payload", "Rank", "Description")
            for database in all_payloads:
                number = 0
                payloads_data = []
                payloads = all_payloads[database]

                for payload in sorted(payloads):
                    if keyword in payload or keyword in payloads[payload]['Description']:
                        name = payload.replace(keyword, self.colors.RED + keyword + self.colors.END)
                        description = payloads[payload]['Description'].replace(keyword, self.colors.RED + keyword + self.colors.END)

                        payloads_data.append((number, payloads[payload]['Category'], name,
                                              payloads[payload]['Rank'], description))
                        payloads_shorts.update({number: payload})

                        number += 1
                if payloads_data:
                    self.tables.print_table(f"Payloads ({database})", headers, *payloads_data)
                    self.local_storage.set("payload_shorts", payloads_shorts)

    def show_sessions(self):
        sessions = self.local_storage.get("sessions")
        if sessions:
            sessions_data = []
            headers = ("ID", "Platform", "Architecture", "Type", "Host", "Port")
            for session_id in sessions:
                session_platform = sessions[session_id]['platform']
                session_architecture = sessions[session_id]['architecture']
                session_type = sessions[session_id]['type']
                host = sessions[session_id]['host']
                port = sessions[session_id]['port']

                sessions_data.append((session_id, session_platform, session_architecture, session_type, host, port))
            self.tables.print_table("Opened Sessions", headers, *sessions_data)
        else:
            self.badges.print_warning("No opened sessions available.")

    def show_module_information(self, current_module_details):
        current_module = current_module_details

        authors = ""
        for author in current_module['Authors']:
            authors += author + ", "
        authors = authors[:-2]

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
            options_data = []
            headers = ("Option", "Value", "Required", "Description")
            options = current_module.options

            for option in sorted(options):
                value, required = options[option]['Value'], options[option]['Required']
                if required:
                    required = "yes"
                else:
                    required = "no"
                if not value and value != 0:
                    value = ""
                options_data.append((option, value, required, options[option]['Description']))
            self.tables.print_table(f"Module Options ({current_module.details['Module']})", headers, *options_data)

        if hasattr(current_module, "payload"):
            if hasattr(self.payloads.get_current_payload(), "options"):
                options_data = []
                headers = ("Option", "Value", "Required", "Description")
                current_payload = self.payloads.get_current_payload()
                if current_payload:
                    for option in sorted(current_payload.options):
                        value, required = current_payload.options[option]['Value'], \
                                          current_payload.options[option]['Required']
                        if required:
                            required = "yes"
                        else:
                            required = "no"
                        if not value and value != 0:
                            value = ""
                        options_data.append((option, value, required, current_payload.options[option]['Description']))
                    self.tables.print_table(f"Payload Options ({current_payload.details['Payload']})", headers,
                                            *options_data)
