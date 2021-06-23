#!/usr/bin/env python3

#
# This command requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.core.base.storage import LocalStorage
from hatsploit.command import Command
from hatsploit.core.modules.modules import Modules


class HatSploitCommand(Command):
    modules = Modules()
    local_storage = LocalStorage()

    details = {
        'Category': "core",
        'Name': "help",
        'Authors': [
            'Ivan Nikolsky (enty8080)'
        ],
        'Description': "Show available commands.",
        'Usage': "help",
        'MinArgs': 0
    }

    def format_base_commands(self):
        commands_data = dict()
        headers = ("Command", "Description")
        commands = self.local_storage.get("commands")
        for command in sorted(commands.keys()):
            label = commands[command].details['Category']
            commands_data[label] = list()
        for command in sorted(commands.keys()):
            label = commands[command].details['Category']
            commands_data[label].append((command, commands[command].details['Description']))
        for label in sorted(commands_data.keys()):
            self.print_table(label.title() + " Commands", headers, *commands_data[label])

    def format_plugin_commands(self):
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
                    self.print_table(label.title() + " Commands", headers, *commands_data[label])

    def format_custom_commands(self):
        current_module = self.modules.get_current_module_object()
        if hasattr(current_module, "commands"):
            commands_data = list()
            headers = ("Command", "Description")
            commands = current_module.commands
            for command in sorted(commands.keys()):
                commands_data.append((command, commands[command]['Description']))
            self.print_table("Custom Commands", headers, *commands_data)

    def run(self, argc, argv):
        self.format_base_commands()
        if self.modules.check_current_module():
            self.format_custom_commands()
        if self.local_storage.get("loaded_plugins"):
            self.format_plugin_commands()
