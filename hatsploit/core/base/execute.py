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

import os
import subprocess
import sys

from hatsploit.lib.storage import LocalStorage
from hatsploit.core.cli.badges import Badges
from hatsploit.core.cli.fmt import FMT
from hatsploit.lib.modules import Modules


class Execute:
    def __init__(self):
        self.fmt = FMT()
        self.badges = Badges()
        self.local_storage = LocalStorage()
        self.modules = Modules()

    def execute_command(self, commands, arguments):
        if commands:
            if not self.execute_builtin_method(commands, arguments):
                if not self.execute_core_command(commands, arguments):
                    if not self.execute_module_command(commands, arguments):
                        if not self.execute_plugin_command(commands, arguments):
                            self.badges.output_error("Unrecognized command: " + commands[0] + "!")

    def execute_from_file(self, input_file):
        if os.path.exists(input_file):
            file = open(input_file, 'r')
            file_text = file.read().split('\n')
            file.close()

            for line in file_text:
                commands = self.fmt.format_commands(line)
                arguments = commands[1:]

                self.execute_command(commands, arguments)

    def execute_builtin_method(self, commands, arguments):
        if commands[0][0] == '!':
            if len(commands[0]) > 1:
                commands[0] = commands[0].replace('!', '', 1)
                self.execute_system(commands)
            else:
                self.badges.output_usage("!<command>")
            return True
        return False

    def execute_system(self, commands):
        self.badges.output_process("Executing system command: " + commands[0] + "\n")
        try:
            subprocess.call(commands)
        except Exception:
            self.badges.output_error("Unrecognized system command: " + commands[0] + "!")

    def execute_core_command(self, commands, arguments):
        if self.local_storage.get("commands"):
            if commands[0] in self.local_storage.get("commands").keys():
                command = self.local_storage.get("commands")[commands[0]]
                if (len(commands) - 1) < command.details['MinArgs']:
                    self.badges.output_usage(command.details['Usage'])
                else:
                    command.run(len(arguments), arguments)
                return True
        return False

    def execute_module_command(self, commands, arguments):
        if self.modules.check_current_module():
            if hasattr(self.modules.get_current_module_object(), "commands"):
                if commands[0] in self.modules.get_current_module_object().commands.keys():
                    command_object = self.modules.get_current_module_object()
                    command = self.modules.get_current_module_object().commands[commands[0]]
                    self.parse_and_execute_command(commands, command, arguments, command_object)
                    return True
        return False

    def execute_plugin_command(self, commands, arguments):
        if self.local_storage.get("loaded_plugins"):
            for plugin in self.local_storage.get("loaded_plugins").keys():
                if hasattr(self.local_storage.get("loaded_plugins")[plugin], "commands"):
                    for label in self.local_storage.get("loaded_plugins")[plugin].commands.keys():
                        if commands[0] in self.local_storage.get("loaded_plugins")[plugin].commands[label].keys():
                            command_object = self.local_storage.get("loaded_plugins")[plugin]
                            command = command_object.commands[label][commands[0]]
                            self.parse_and_execute_command(commands, command, arguments, command_object)
                            return True
        return False

    def parse_and_execute_command(self, commands, command, arguments, command_object):
        if hasattr(command_object, commands[0]):
            if (len(commands) - 1) < command['MinArgs']:
                self.badges.output_usage(command['Usage'])
            else:
                getattr(command_object, commands[0])(len(arguments), arguments)
        else:
            self.badges.output_error("Failed to execute command!")
