#!/usr/bin/env python3

#
# MIT License
#
# Copyright (c) 2020-2022 EntySec
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
from hatsploit.lib.encoders import Encoders
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
    encoders = Encoders()
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
        current_module = self.modules.get_current_module()
        if hasattr(current_module, "commands"):
            commands_data = []
            headers = ("Command", "Description")
            commands = current_module.commands
            for command in sorted(commands):
                commands_data.append((command, commands[command]['Description']))
            self.tables.print_table("Module Commands", headers, *commands_data)

    def show_all_commands(self):
        self.show_interface_commands()
        if self.modules.get_current_module():
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

    def show_encoder_databases(self):
        if self.local_storage.get("connected_encoder_databases"):
            databases_data = []
            number = 0
            headers = ("Number", "Name", "Path")
            databases = self.local_storage.get("connected_encoder_databases")

            for name in databases:
                databases_data.append((number, name, databases[name]['path']))
                number += 1
            self.tables.print_table("Connected Encoder Databases", headers, *databases_data)
        else:
            self.badges.print_warning("No encoder database connected.")

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
        headers = ("Number", "Plugin", "Name")
        plugins_shorts = {}

        for database in sorted(all_plugins):
            number = 0
            plugins_data = []
            plugins = all_plugins[database]

            for plugin in sorted(plugins):
                plugins_data.append((number, plugins[plugin]['Plugin'], plugins[plugin]['Name']))
                plugins_shorts.update({number: plugins[plugin]['Plugin']})
                number += 1

            self.tables.print_table(f"Plugins ({database})", headers, *plugins_data)
            self.local_storage.set("plugin_shorts", plugins_shorts)

    def show_encoders(self):
        all_encoders = self.local_storage.get("encoders")
        headers = ("Number", "Encoder", "Name")
        encoders_shorts = {}

        for database in sorted(all_encoders):
            number = 0
            encoders_data = []
            encoders = all_encoders[database]

            for encoder in sorted(encoders):
                encoders_data.append((number, encoders[encoder]['Encoder'], encoders[encoder]['Name']))
                encoders_shorts.update({number: encoders[encoder]['Encoder']})
                number += 1

            self.tables.print_table(f"Encoders ({database})", headers, *encoders_data)
            self.local_storage.set("encoder_shorts", encoders_shorts)

    def show_modules(self, category=None):
        all_modules = self.local_storage.get("modules")
        headers = ("Number", "Category", "Module", "Rank", "Name")
        modules_shorts = {}

        for database in sorted(all_modules):
            number = 0
            modules_data = []
            modules = all_modules[database]

            for module in sorted(modules):
                if category:
                    if category == modules[module]['Category']:
                        modules_data.append((number, modules[module]['Category'], modules[module]['Module'],
                                             modules[module]['Rank'], modules[module]['Name']))
                        modules_shorts.update({number: modules[module]['Module']})
                        number += 1
                else:
                    modules_data.append((number, modules[module]['Category'], modules[module]['Module'],
                                         modules[module]['Rank'], modules[module]['Name']))
                    modules_shorts.update({number: modules[module]['Module']})
                    number += 1

            if category:
                self.tables.print_table(f"{category.title()} Modules ({database})", headers, *modules_data)
            else:
                self.tables.print_table(f"Modules ({database})", headers, *modules_data)

            self.local_storage.set("module_shorts", modules_shorts)

    def show_payloads(self, category=None):
        all_payloads = self.local_storage.get("payloads")
        headers = ("Number", "Category", "Payload", "Rank", "Name")
        payloads_shorts = {}

        for database in sorted(all_payloads):
            number = 0
            payloads_data = []
            payloads = all_payloads[database]

            for payload in sorted(payloads):
                if category:
                    if category == payloads[payload]['Category']:
                        payloads_data.append((number, payloads[payload]['Category'], payloads[payload]['Payload'],
                                              payloads[payload]['Rank'], payloads[payload]['Name']))
                        payloads_shorts.update({number: payloads[payload]['Payload']})
                        number += 1
                else:
                    payloads_data.append((number, payloads[payload]['Category'], payloads[payload]['Payload'],
                                          payloads[payload]['Rank'], payloads[payload]['Name']))
                    payloads_shorts.update({number: payloads[payload]['Payload']})
                    number += 1

            if category:
                self.tables.print_table(f"{category.title()} Payloads ({database})", headers, *payloads_data)
            else:
                self.tables.print_table(f"Payloads ({database})", headers, *payloads_data)

            self.local_storage.set("payload_shorts", payloads_shorts)

    def show_search_plugins(self, keyword):
        all_plugins = self.local_storage.get("plugins")
        plugins_shorts = {}

        if all_plugins:
            headers = ("Number", "Plugin", "Name")
            for database in all_plugins:
                number = 0
                plugins_data = []
                plugins = all_plugins[database]

                for plugin in sorted(plugins):
                    if keyword in plugins[plugin]['Plugin'] or keyword in plugins[plugin]['Name']:
                        name = plugins[plugin]['Plugin'].replace(keyword, self.colors.RED + keyword + self.colors.END)
                        description = plugins[plugin]['Name'].replace(
                            keyword, self.colors.RED + keyword + self.colors.END)

                        plugins_data.append((number, name, description))
                        plugins_shorts.update({number: plugins[plugin]['Plugin']})

                        number += 1
                if plugins_data:
                    self.tables.print_table(f"Plugins ({database})", headers, *plugins_data)
                    self.local_storage.set("plugin_shorts", plugins_shorts)

    def show_search_encoders(self, keyword):
        all_encoders = self.local_storage.get("encoders")
        encoders_shorts = {}

        if all_encoders:
            headers = ("Number", "Encoder", "Name")
            for database in all_encoders:
                number = 0
                encoders_data = []
                encoders = all_encoders[database]

                for encoder in sorted(encoders):
                    if keyword in encoders[encoder]['Encoder'] or keyword in encoders[encoder]['Name']:
                        name = encoders[encoder]['Encoder'].replace(
                            keyword, self.colors.RED + keyword + self.colors.END)
                        description = encoders[encoder]['Name'].replace(
                            keyword, self.colors.RED + keyword + self.colors.END)

                        encoders_data.append((number, name, description))
                        encoders_shorts.update({number: encoders[encoder]['Encoder']})

                        number += 1
                if encoders_data:
                    self.tables.print_table(f"Encoders ({database})", headers, *encoders_data)
                    self.local_storage.set("encoder_shorts", encoders_shorts)

    def show_search_modules(self, keyword):
        all_modules = self.local_storage.get("modules")
        modules_shorts = {}

        if all_modules:
            headers = ("Number", "Module", "Rank", "Name")
            for database in all_modules:
                number = 0
                modules_data = []
                modules = all_modules[database]

                for module in sorted(modules):
                    if keyword in modules[module]['Module'] or keyword in modules[module]['Name']:
                        name = modules[module]['Module'].replace(keyword, self.colors.RED + keyword + self.colors.END)
                        description = modules[module]['Name'].replace(
                            keyword, self.colors.RED + keyword + self.colors.END)

                        modules_data.append((number, name, modules[module]['Rank'], description))
                        modules_shorts.update({number: modules[module]['Module']})

                        number += 1
                if modules_data:
                    self.tables.print_table(f"Modules ({database})", headers, *modules_data)
                    self.local_storage.set("module_shorts", modules_shorts)

    def show_search_payloads(self, keyword):
        all_payloads = self.local_storage.get("payloads")
        payloads_shorts = {}

        if all_payloads:
            headers = ("Number", "Category", "Payload", "Rank", "Name")
            for database in all_payloads:
                number = 0
                payloads_data = []
                payloads = all_payloads[database]

                for payload in sorted(payloads):
                    if keyword in payloads[payload]['Payload'] or keyword in payloads[payload]['Name']:
                        name = payloads[payload]['Payload'].replace(
                            keyword, self.colors.RED + keyword + self.colors.END)
                        description = payloads[payload]['Name'].replace(
                            keyword, self.colors.RED + keyword + self.colors.END)

                        payloads_data.append((number, payloads[payload]['Category'], name,
                                              payloads[payload]['Rank'], description))
                        payloads_shorts.update({number: payloads[payload]['Payload']})

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

    def show_information(self, details):
        if 'Name' in details:
            self.badges.print_information(f"Name: {details['Name']}")
        if 'Module' in details:
            self.badges.print_information(f"Module: {details['Name']}")


    def show_options(self):
        current_module = self.modules.get_current_module()

        if not current_module:
            self.badges.print_warning("No module selected.")
            return

        if not hasattr(current_module, "options") and not hasattr(current_module, "payload"):
            self.badges.print_warning("Module has no options.")
            return

        if not hasattr(current_module, "options") and not hasattr(self.payloads.get_current_payload(), "options"):
            self.badges.print_warning("Module has no options.")
            return

        headers = ("Option", "Value", "Required", "Description")

        if hasattr(current_module, "options"):
            options_data = []
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
            current_payload = self.payloads.get_current_payload()
            current_encoder = self.encoders.get_current_encoder()

            if current_payload and hasattr(current_payload, "options"):
                options_data = []

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

            if current_encoder and hasattr(current_encoder, "options"):
                options_data = []

                for option in sorted(current_encoder.options):
                    value, required = current_encoder.options[option]['Value'], \
                                      current_encoder.options[option]['Required']
                    if required:
                        required = "yes"
                    else:
                        required = "no"
                    if not value and value != 0:
                        value = ""
                    options_data.append((option, value, required, current_encoder.options[option]['Description']))
                self.tables.print_table(f"Encoder Options ({current_payload.details['Payload']})", headers,
                                        *options_data)
