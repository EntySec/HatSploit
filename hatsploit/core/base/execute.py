"""
MIT License

Copyright (c) 2020-2024 EntySec

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os
import subprocess
import sys

from typing import Any, Tuple, Union
from badges import Badges, Tables

from hatsploit.lib.jobs import Jobs
from hatsploit.lib.modules import Modules
from hatsploit.lib.show import Show
from hatsploit.lib.storage import LocalStorage


class Execute(object):
    """ Subclass of hatsploit.core.base module.

    This subclass of hatsploit.core.base module is intended for
    providing interfaces for executing commands in HatSploit interpreter.
    """

    def __init__(self) -> None:
        super().__init__()

        self.jobs = Jobs()
        self.badges = Badges()
        self.tables = Tables()
        self.local_storage = LocalStorage()
        self.modules = Modules()
        self.show = Show()

    def execute_command(self, command: list) -> None:
        """ Execute command.

        :param list command: command with arguments
        :return None: None
        """

        if command:
            if not self.execute_builtin_method(command):
                if not self.execute_core_command(command):
                    if not self.execute_module_command(command):
                        if not self.execute_plugin_command(command):
                            self.badges.print_error(
                                f"Unrecognized command: {command[0]}!"
                            )

    def execute_builtin_method(self, command: list) -> bool:
        """ Execute command as interpreter builtin method.

        :param list command: command with arguments
        :return bool: status, True if success else False
        """

        if command[0][0] == '#':
            return True

        if command[0][0] == '?':
            self.show.show_all_commands()
            return True

        if command[0][0] == '&':
            command[0] = command[0][1:]

            self.jobs.create_job(
                command[0], None, self.execute_command, [command], hidden=True
            )

            return True

        if command[0][0] == '!':
            if len(command[0]) > 1:
                command[0] = command[0].replace('!', '', 1)
                self.execute_system(command)

            else:
                self.badges.print_usage("!<command>")

            return True
        return False

    def execute_system(self, command: list) -> None:
        """ Execute command as system.

        :param list command: command with arguments
        :return None: None
        """

        self.badges.print_process(f"Executing system command: {command[0]}\n")
        try:
            subprocess.call(command)
        except Exception:
            self.badges.print_error(f"Unrecognized system command: {command[0]}!")

    def check_command(self, command: list, handler: dict) -> Tuple[bool, Union[str, list, None]]:
        """ Check if command or shortcut exists.

        Note: handler is a dictionary containing command names as keys and
        command objects as items.

        :param list command: command with arguments
        :param dict handler: handler to use
        :return Tuple[bool, Union[str, list, None]]: None if not found or tuple of status and if command is single,
            object, otherwise list of similar commands.
        """

        commands = {}

        for name, object in handler.items():
            for i in range(len(name) + 1):
                prefix = name[:i]

                if prefix not in commands:
                    commands[prefix] = name

                elif commands[prefix] != name:
                    commands[prefix] = None

        if command[0] in commands:
            result = commands[command[0]]

            if result:
                return True, result

            else:
                conflict = [name for name, object in handler.items() if name.startswith(command[0])]

                if command[0] in conflict:
                    return True, command[0]
                else:
                    return False, conflict

        return False, None

    def execute_custom_command(self, command: list, handler: dict) -> bool:
        """ Execute command via custom handler.

        Note: handler is a dictionary containing command names as keys and
        command objects as items.

        :param list command: command with arguments
        :param dict handler: handler to use
        :return bool: status, True if success else False
        """

        if handler:
            status, name = self.check_command(command, handler)

            if status:
                fixed_command = [name, *command[1:]]

                if not self.check_arguments(fixed_command, handler[name].details):
                    self.parse_usage(handler[name].details)
                else:
                    handler[name].run(len(fixed_command), fixed_command)

                return True

            if name is not None:
                self.badges.print_warning(f"Did you mean? {', '.join(name)}")

        return False

    @staticmethod
    def check_arguments(command: list, details: dict) -> bool:
        """ Check if arguments correct for command.

        :param list command: command with arguments
        :param dict details: dictionary of command details
        :return bool: status, True if correct else False
        """

        if (len(command) - 1) < details['MinArgs']:
            return False

        if 'Options' in details:
            if len(command) > 1:
                if command[1] in details['Options']:
                    if (len(command) - 2) < len(
                            details['Options'][command[1]][0].split()
                    ):
                        return False
                else:
                    return False

        if len(command) > 1:
            if command[1] == '?':
                return False

        return True

    def parse_usage(self, details: dict) -> None:
        """ Print usage for specific command details.

        :param dict details: dictionary of command details
        :return None: None
        """

        self.badges.print_usage(details['Usage'])

        if 'Options' in details:
            headers = ('Option', 'Arguments', 'Description')
            data = []

            for option in details['Options']:
                info = details['Options'][option]
                data.append((option, info[0], info[1]))

            self.tables.print_table('Options', headers, *data)

    def execute_core_command(self, command: list) -> bool:
        """ Execute core command.

        :param list command: command with arguments
        :return bool: status, True if success else False
        """

        return self.execute_custom_command(
            command, self.local_storage.get("commands"))

    def execute_module_command(self, command: list) -> bool:
        """ Execute current module command.

        :param list command: command with arguments
        :return bool: status, True if success else False
        """

        module = self.modules.get_current_module()

        if module:
            if hasattr(module, "commands"):
                status, name = self.check_command(command, module.commands)

                if status:
                    fixed_command = [name, *command[1:]]
                    self.parse_and_execute_command(
                        fixed_command, module.commands[name], module)

                    return True

                if name is not None:
                    self.badges.print_warning(f"Did you mean? {', '.join(name)}")

        return False

    def execute_plugin_command(self, command: list) -> bool:
        """ Execute loaded plugin command.

        :param list command: command with arguments
        :return bool: status, True if success else False
        """

        return self.execute_custom_plugin_command(
            command, self.local_storage.get("loaded_plugins"))

    def execute_custom_plugin_command(self, command: list, plugins: dict) -> bool:
        """ Execute custom plugin command.

        :param list command: command with arguments
        :param dict plugins: plugins where to search for command
        :return bool: status, True if success else False
        """

        if plugins:
            for plugin in plugins:
                plugin = plugins[plugin]

                for label in plugin.commands:
                    status, name = self.check_command(command, plugin.commands[label])

                    if status:
                        fixed_command = [name, *command[1:]]
                        details = plugin.commands[label][name]

                        self.parse_and_execute_command(
                            fixed_command, details, plugin)

                        return True

                    if name is not None:
                        self.badges.print_warning(f"Did you mean? {', '.join(name)}")

        return False

    def parse_and_execute_command(self, command: list, details: dict, handle: Any) -> None:
        """ Parse command details and execute handle.

        :param list command: command with arguments
        :param dict details: command details
        :param Any handle: something that has command name as an
        executable attribute, entry point
        :return None: None
        """

        if hasattr(handle, command[0]):
            if not self.check_arguments(command, details):
                self.parse_usage(details)
            else:
                getattr(handle, command[0])(len(command), command)
        else:
            self.badges.print_error("Failed to execute command!")
