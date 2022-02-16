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

import readline

from hatsploit.core.cli.fmt import FMT
from hatsploit.lib.storage import LocalStorage


class Completer:
    fmt = FMT()
    local_storage = LocalStorage()

    matches = None

    def completer(self, text, state):
        if state == 0:
            original_line = readline.get_line_buffer()
            line = original_line.lstrip()

            stripped = len(original_line) - len(line)

            start_index = readline.get_begidx() - stripped
            end_index = readline.get_endidx() - stripped

            if start_index > 0:
                command = self.fmt.format_commands(line)

                if command[0] == "":
                    complete_function = self.default_completer
                else:
                    if command[0] in ['use', 'info']:
                        complete_function = self.modules_completer
                    elif command[0] in ['load', 'unload']:
                        complete_function = self.plugins_completer
                    else:
                        complete_function = self.default_completer
            else:
                complete_function = self.commands_completer

            self.matches = complete_function(text, line, start_index, end_index)

        try:
            return self.matches[state]
        except IndexError:
            return None

    def plugins_completer(self, text, line, start_index, end_index):
        return [plugin for plugin in self.local_storage.get("plugins")['plugins'] if plugin.startswith(text)]

    def payloads_completer(self, text, line, start_index, end_index):
        return [payload for payload in self.local_storage.get("payloads")['payloads'] if payload.startswith(text)]

    def modules_completer(self, text, line, start_index, end_index):
        return [module for module in self.local_storage.get("modules")['modules'] if module.startswith(text)]

    def commands_completer(self, text, line, start_index, end_index):
        return [command for command in self.local_storage.get("commands") if command.startswith(text)]

    def default_completer(self, *ignored):
        return []
