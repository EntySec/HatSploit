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

import readline
import os
import sys

from badges import Badges
from pex.string import String

from hatsploit.core.base.execute import Execute

from hatsploit.core.utils.ui.banner import Banner
from hatsploit.core.utils.ui.completer import Completer
from hatsploit.core.utils.ui.tip import Tip

from hatsploit.lib.config import Config
from hatsploit.lib.modules import Modules
from hatsploit.lib.runtime import Runtime
from hatsploit.lib.storage import LocalStorage


class Console(object):
    """ Subclass of hatsploit.core.base module.

    This subclass of hatsploit.lib.base module represents console
    handler for HatSploit.
    """

    def __init__(self) -> None:
        super().__init__()

        self.execute = Execute()

        self.string = String()
        self.badges = Badges()

        self.completer = Completer()
        self.banner = Banner()
        self.tip = Tip()

        self.runtime = Runtime()
        self.config = Config()
        self.modules = Modules()
        self.local_storage = LocalStorage()

        self.history = self.config.path_config['history_path']
        self.prompt = self.config.core_config['details']['prompt']

        self.handler_options = {'Module': {}, 'Payload': {}}

        self.completion = None

    def shell_execute(self) -> None:
        """ Start HatSploit shell interpreter.

        :return None: None
        """

        if not self.modules.get_current_module():
            prompt = f'[{self.prompt}]> '
        else:
            module = self.modules.get_current_module()

            category = module.details['Category']
            name = module.details['Name']

            prompt = f'[{self.prompt}: {category}: %red{name}%end]> '
        commands = self.badges.input_empty(prompt)

        self.runtime.update()
        self.execute.execute_command(self.string.split_args(commands))
        self.runtime.update()

        if self.local_storage.get("history"):
            readline.write_history_file(self.history)

    def shell(self, history: bool = True, header: bool = True) -> None:
        """ Configure HatSploit shell interpreter and start it.

        :param bool history: enable history
        :param bool header: print header
        :return None: None
        """

        if history:
            self.launch_history()
        if header:
            self.show_header()

        while True:
            self.runtime.catch(self.shell_execute)

    def launch_history(self) -> None:
        """ Setup history and tab-completion for
        HatSploit shell interpreter.

        :return None: None
        """

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

    def show_header(self) -> None:
        """ Print HatSploit shell interpreter header.

        :return None: None
        """

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
                header += f"    --=[ %yellowHatSploit Framework {version} {codename} (https://hatsploit.com)%end\n"
            else:
                header += f"    --=[ %yellowHatSploit Framework {version}%end\n"
            header += (
                "--==--=[ Developed by EntySec (%linehttps://entysec.com%end)\n"
            )
            header += f"    --=[ {modules_total} modules | {payloads_total} payloads "
            header += f"| {encoders_total} encoders | {plugins_total} plugins"
            header += "%end"

            self.badges.print_empty(header)

        if self.config.core_config['console']['tip']:
            self.tip.print_random_tip()

    def script(self, input_files: list, shell: bool = True) -> None:
        """ Execute HatSploit script(s).

        :param list input_files: list of filenames of files
        containing HatSploit scripts
        :param bool shell: True to launch shell interpreter
        after all scripts executed else False
        :return None: None
        """

        self.show_header()

        for input_file in input_files:
            if os.path.exists(input_file):
                file = open(input_file, 'r')
                file_text = file.read().split('\n')
                file.close()

                for line in file_text:
                    commands = self.string.split_args(line)

                    self.runtime.update()
                    self.runtime.catch(
                        self.execute.execute_command(commands))
                    self.runtime.update()

        if shell:
            self.shell(header=False)
