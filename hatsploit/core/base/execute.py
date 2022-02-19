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

import os
import subprocess
import sys

from hatsploit.core.cli.badges import Badges
from hatsploit.core.cli.fmt import FMT
from hatsploit.lib.jobs import Jobs
from hatsploit.lib.modules import Modules
from hatsploit.lib.storage import LocalStorage
from hatsploit.lib.show import Show


class Execute:
    jobs = Jobs()
    fmt = FMT()
    badges = Badges()
    local_storage = LocalStorage()
    modules = Modules()
    show = Show()

    def execute_command(self, commands):
        if commands:
            if not self.execute_builtin_method(commands):
                if not self.execute_core_command(commands):
                    if not self.execute_module_command(commands):
                        if not self.execute_plugin_command(commands):
                            self.badges.print_error(f"Unrecognized command: {commands[0]}!")

    def execute_builtin_method(self, commands):
        if commands[0][0] == '#':
            return True
        if commands[0][0] == '?':
            self.show.show_all_commands()
            return True
        if commands[0][0] == '&':
            commands[0] = commands[0][1:]

            self.jobs.create_job(
                commands[0],
                None,
                self.execute_command,
                [commands],
                True
            )

            return True
        if commands[0][0] == '!':
            if len(commands[0]) > 1:
                commands[0] = commands[0].replace('!', '', 1)
                self.execute_system(commands)
            else:
                self.badges.print_usage("!<command>")
            return True
        return False

    def execute_system(self, commands):
        self.badges.print_process(f"Executing system command: {commands[0]}\n")
        try:
            subprocess.call(commands)
        except Exception:
            self.badges.print_error(f"Unrecognized system command: {commands[0]}!")

    def execute_custom_command(self, commands, handler):
        if handler:
            if commands[0] in handler:
                command = handler[commands[0]]
                if (len(commands) - 1) < command.details['MinArgs']:
                    self.parse_usage(command.details)
                else:
                    command.run(len(commands), commands)
                return True
        return False

    def parse_usage(self, details):
        if 'Usage' in details:
            self.badges.print_usage(details['Usage'])

        elif 'Options' in details:
            self.badges.print_usage(f"{details['Name']} <option> [arguments]\n")
            max_option = max(details['Options'], key=len)

            for option in details['Options']:
                description = details['Options'][option]

                if option == max_option:
                    self.badges.print_empty(f"  {option}  {description}")
                else:
                    self.badges.print_empty(f"  {option}{' ' * len(max_option)}{description}")

            self.badges.print_empty()

    def execute_core_command(self, commands):
        return self.execute_custom_command(commands, self.local_storage.get("commands"))

    def execute_module_command(self, commands):
        if self.modules.check_current_module():
            if hasattr(self.modules.get_current_module_object(), "commands"):
                if commands[0] in self.modules.get_current_module_object().commands:
                    command_object = self.modules.get_current_module_object()
                    command = self.modules.get_current_module_object().commands[commands[0]]
                    self.parse_and_execute_command(commands, command, command_object)
                    return True
        return False

    def execute_plugin_command(self, commands):
        if self.local_storage.get("loaded_plugins"):
            for plugin in self.local_storage.get("loaded_plugins"):
                if hasattr(self.local_storage.get("loaded_plugins")[plugin], "commands"):
                    for label in self.local_storage.get("loaded_plugins")[plugin].commands:
                        if commands[0] in self.local_storage.get("loaded_plugins")[plugin].commands[label]:
                            command_object = self.local_storage.get("loaded_plugins")[plugin]
                            command = command_object.commands[label][commands[0]]
                            self.parse_and_execute_command(commands, command, command_object)
                            return True
        return False

    def parse_and_execute_command(self, commands, command, command_object):
        if hasattr(command_object, commands[0]):
            if (len(commands) - 1) < command['MinArgs']:
                self.parse_usage(command)
            else:
                getattr(command_object, commands[0])(len(commands), commands)
        else:
            self.badges.print_error("Failed to execute command!")
