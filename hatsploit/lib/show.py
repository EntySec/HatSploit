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

from hatsploit.core.cli.badges import Badges
from hatsploit.core.cli.tables import Tables


class Show:
    jobs = Jobs()
    local_storage = LocalStorage()
    modules = Modules()

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
