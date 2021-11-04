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

from hatsploit.lib.storage import LocalStorage
from hatsploit.lib.modules import Modules

from hatsploit.core.db.importer import Importer
from hatsploit.core.cli.badges import Badges
from hatsploit.core.cli.tables import Tables
from hatsploit.core.base.execute import Execute


class Commands:
    local_storage = LocalStorage()
    modules = Modules()

    importer = Importer()
    badges = Badges()
    tables = Tables()
    execute = Execute()

    def load_commands(self, path):
        return self.importer.import_commands(path)

    def execute_command(self, commands):
        self.execute.execute_command(commands)

    def execute_custom_command(self, commands, handler):
        if commands:
            if not self.execute.execute_builtin_method(commands):
                if not self.execute.execute_custom_command(commands, handler):
                    self.badges.print_error("Unrecognized command: " + commands[0] + "!")

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
        self.show_custom_commands(self.local_storage.get("commands"))

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
