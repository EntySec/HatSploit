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
import readline
import sys

from hatsploit.core.base.execute import Execute

from hatsploit.core.cli.fmt import FMT
from hatsploit.core.cli.badges import Badges

from hatsploit.core.utils.ui.completer import Completer
from hatsploit.core.utils.ui.banner import Banner
from hatsploit.core.utils.ui.tip import Tip

from hatsploit.lib.runtime import Runtime
from hatsploit.lib.config import Config
from hatsploit.lib.modules import Modules
from hatsploit.lib.storage import LocalStorage


class Console:
    execute = Execute()

    fmt = FMT()
    badges = Badges()

    completer = Completer()
    banner = Banner()
    tip = Tip()

    runtime = Runtime()
    config = Config()
    modules = Modules()
    local_storage = LocalStorage()

    history = config.path_config['history_path']
    prompt = config.core_config['details']['prompt']

    handler_options = {
        'Module': {},
        'Payload': {}
    }

    completion = None

    def shell_execute(self):
        if not self.modules.get_current_module():
            prompt = f'({self.prompt})> '
        else:
            current_module = self.modules.get_current_module()

            category = current_module.details['Category']
            name = current_module.details['Name']

            prompt = f'({self.prompt}: {category}: %red{name}%end)> '
        commands = self.badges.input_empty(prompt)

        self.runtime.update()
        self.execute.execute_command(commands)
        self.runtime.update()

        if self.local_storage.get("history"):
            readline.write_history_file(self.history)

    def shell(self, start=True, history=True, header=True):
        if start:
            if not self.runtime.catch(self.runtime.start):
                return

        if history:
            self.launch_history()
        if header:
            self.show_header()

        while True:
            self.runtime.catch(self.shell_execute)

    def launch_history(self):
        readline.set_auto_history(False)

        using_history = self.local_storage.get("history")
        if using_history:
            readline.set_auto_history(True)

            if not os.path.exists(self.history):
                open(self.history, 'w').close()
            readline.read_history_file(self.history)

        readline.set_completer(self.completer.completer)
        readline.set_completer_delims(" \t\n;")

        readline.parse_and_bind("tab: complete")

    def show_header(self):
        version = self.config.core_config['details']['version']
        codename = self.config.core_config['details']['codename']

        if self.config.core_config['console']['clear']:
            self.badges.print_empty("%clear", end='')

        if self.config.core_config['console']['banner']:
            self.banner.print_random_banner()

        if self.config.core_config['console']['header']:
            plugins = self.local_storage.get("plugins")
            modules = self.local_storage.get("modules")
            payloads = self.local_storage.get("payloads")
            encoders = self.local_storage.get("encoders")

            plugins_total = 0
            modules_total = 0
            payloads_total = 0
            encoders_total = 0

            if payloads:
                for database in payloads:
                    payloads_total += len(payloads[database])
            if encoders:
                for database in encoders:
                    encoders_total += len(encoders[database])
            if plugins:
                for database in plugins:
                    plugins_total += len(plugins[database])
            if modules:
                for database in modules:
                    modules_total += len(modules[database])

            header = ""
            header += "%end"
            if codename:
                header += f"    --=( %yellowHatSploit Framework {version} {codename}%end\n"
            else:
                header += f"    --=( %yellowHatSploit Framework {version}%end\n"
            header += "--==--=( Developed by EntySec (%linehttps://entysec.netlify.app/%end)\n"
            header += f"    --=( {modules_total} modules | {payloads_total} payloads "
            header += f"| {encoders_total} encoders | {plugins_total} plugins"
            header += "%end"

            self.badges.print_empty(header)

        if self.config.core_config['console']['tip']:
            self.tip.print_random_tip()

    def script(self, input_files, shell=False):
        if self.runtime.catch(self.runtime.start):
            self.show_header()

            for input_file in input_files:
                if os.path.exists(input_file):
                    file = open(input_file, 'r')
                    file_text = file.read().split('\n')
                    file.close()

                    for line in file_text:
                        commands = self.fmt.format_commands(line)

                        self.runtime.update()
                        self.execute.execute_command(commands)
                        self.runtime.update()

            if shell:
                self.shell(
                    start=False,
                    header=False
                )
