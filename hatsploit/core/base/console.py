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
import sys
import readline

from hatsploit.lib.config import Config
from hatsploit.core.base.exceptions import Exceptions
from hatsploit.core.base.execute import Execute
from hatsploit.core.base.io import IO
from hatsploit.lib.jobs import Jobs
from hatsploit.core.base.loader import Loader
from hatsploit.lib.storage import LocalStorage
from hatsploit.core.cli.badges import Badges
from hatsploit.core.cli.colors import Colors
from hatsploit.lib.modules import Modules
from hatsploit.core.utils.ui.banner import Banner
from hatsploit.core.utils.ui.tip import Tip


class Console:
    def __init__(self):
        self.io = IO()
        self.tip = Tip()
        self.jobs = Jobs()
        self.execute = Execute()
        self.loader = Loader()
        self.config = Config()
        self.badges = Badges()
        self.banner = Banner()
        self.colors = Colors()
        self.local_storage = LocalStorage()
        self.modules = Modules()
        self.exceptions = Exceptions()

        self.history = self.config.path_config['history_path']

    def check_install(self):
        if os.path.exists(self.config.path_config['root_path']):
            return True
        self.badges.print_error("HatSploit is not installed!")
        self.badges.print_information("Consider running ./install.sh")
        return False

    def start_hsf(self):
        try:
            self.loader.load_all()
        except Exception:
            sys.exit(1)

    def launch_menu(self):
        while True:
            try:
                if not self.modules.check_current_module():
                    prompt = '(hsf)> '
                else:
                    module = self.modules.get_current_module_name()
                    name = self.modules.get_current_module_object().details['Name']
                    prompt = '(hsf: ' + module.split('/')[0] + ': ' + self.colors.RED + name + self.colors.END + ')> '
                commands, arguments = self.io.input(prompt)

                self.jobs.stop_dead()
                self.execute.execute_command(commands, arguments)
                if self.local_storage.get("history"):
                    readline.write_history_file(self.history)

            except (KeyboardInterrupt, EOFError, self.exceptions.GlobalException):
                pass
            except Exception as e:
                self.badges.print_error("An error occurred: " + str(e) + "!")

    def enable_history_file(self):
        if not os.path.exists(self.history):
            open(self.history, 'w').close()
        readline.read_history_file(self.history)

    def launch_history(self):
        readline.set_auto_history(False)

        using_history = self.local_storage.get("history")
        if using_history:
            readline.set_auto_history(True)
            self.enable_history_file()

        readline.parse_and_bind("tab: complete")

    def launch_shell(self):
        version = self.config.core_config['details']['version']
        codename = self.config.core_config['details']['codename']
        if self.config.core_config['console']['clear']:
            self.badges.print_empty(self.colors.CLEAR, end='')

        if self.config.core_config['console']['banner']:
            self.banner.print_random_banner()

        if self.config.core_config['console']['header']:
            plugins = self.local_storage.get("plugins")
            modules = self.local_storage.get("modules")
            payloads = self.local_storage.get("payloads")

            plugins_total = 0
            modules_total = 0
            payloads_total = 0

            if payloads:
                for database in payloads.keys():
                    payloads_total += len(payloads[database])
            if plugins:
                for database in plugins.keys():
                    plugins_total += len(plugins[database])
            if modules:
                for database in modules.keys():
                    modules_total += len(modules[database])

            header = ""
            header += f"{self.colors.END}\n"
            if codename and not codename.isspace():
                header += f"    --=( {self.colors.YELLOW}HatSploit Framework {version} {codename}{self.colors.END}\n"
            else:
                header += f"    --=( {self.colors.YELLOW}HatSploit Framework {version}{self.colors.END}\n"
            header += f"--==--=( Developed by EntySec ({self.colors.LINE}https://entysec.netlify.app/{self.colors.END})\n"
            header += f"    --=( {modules_total} modules | {payloads_total} payloads | {plugins_total} plugins\n"
            header += f"{self.colors.END}"
            self.badges.print_empty(header)

        if self.config.core_config['console']['tip']:
            self.tip.print_random_tip()
            self.badges.print_empty()

    def shell(self):
        self.start_hsf()
        self.launch_history()
        self.launch_shell()
        self.launch_menu()

    def script(self, file, do_shell=False):
        self.start_hsf()
        self.launch_shell()

        with open(file, 'r') as f:
            for command in f.read().split('\n'):
                commands = command.strip().split()
                arguments = list()

                if commands:
                    command = command.replace(commands[0], "", 1).strip()

                    for arg in command.split():
                        arguments.append(arg)

                    self.jobs.stop_dead()
                    self.execute.execute_command(commands, arguments)
        if do_shell:
            self.launch_history()
            self.launch_menu()
