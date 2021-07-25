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
import readline
import sys

from hatsploit.lib.storage import LocalStorage
from hatsploit.core.cli.colors import Colors
from hatsploit.core.cli.fmt import FMT


class IO:
    def __init__(self):
        self.colors = Colors()
        self.local_storage = LocalStorage()
        self.fmt = FMT()

    def output(self, message="", start='\033[1K\r', end='\n'):
        use_spool = self.local_storage.get("spool")

        sys.stdout.write(start + message + end)
        sys.stdout.flush()

        if use_spool:
            with open(spool, 'a') as f:
                f.write(start + message + end)
                f.flush()

        if self.local_storage.get("current_prompt") and self.local_storage.get("active_input"):
            prompt = start + self.local_storage.get("current_prompt") + readline.get_line_buffer()
            sys.stdout.write(prompt)
            sys.stdout.flush()

    def input(self, prompt_message=""):
        use_spool = self.local_storage.get("spool")

        self.local_storage.set("current_prompt", prompt_message)
        self.local_storage.set("active_input", True)

        commands = input(self.colors.REMOVE + prompt_message)
        if use_spool:
            with open(spool, 'a') as f:
                f.write(self.colors.REMOVE + prompt_message + commands)
                f.flush()

        commands = self.fmt.format_commands(commands)
        arguments = list()

        if commands:
            arguments = commands[1:]

        self.local_storage.set("active_input", False)
        return commands, arguments
