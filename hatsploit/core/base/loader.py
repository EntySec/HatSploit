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
import string
import sys
import threading
import time

from hatsploit.lib.config import Config
from hatsploit.core.cli.badges import Badges
from hatsploit.core.db.builder import Builder
from hatsploit.core.db.importer import Importer
from hatsploit.core.utils.update import Update


class Loader:
    def __init__(self):
        self.badges = Badges()
        self.importer = Importer()
        self.builder = Builder()
        self.config = Config()
        self.update = Update()

        self.build = True

    def load_update_process(self):
        check = self.update.check_update()

        if check is None:
            self.badges.print_warning("Could not compare HatSploit versions.")
            time.sleep(1)
            return

        if check:
            self.badges.print_warning("Your HatSploit Framework is out-dated.")
            self.badges.print_information("Consider running hsf --update")
            time.sleep(1)

    def load_components(self):
        if not self.builder.check_base_built() and self.build:
            self.builder.build_base()
        self.importer.import_all(self.build)

    def load_everything(self):
        self.load_components()

    def load_all(self):
        self.load_update_process()
        if not self.builder.check_base_built():
            build = self.badges.input_question("Do you want to build and connect base databases? [y/n] ")
            if build.lower() in ['y', 'yes']:
                self.build = True
            else:
                self.build = False

        loading_process = threading.Thread(target=self.load_everything)
        loading_process.start()
        base_line = "Loading the HatSploit Framework..."
        cycle = 0
        while loading_process.is_alive():
            for char in "/-\|":
                status = base_line + char + "\r"
                cycle += 1
                if status[cycle % len(status)] in list(string.ascii_lowercase):
                    status = status[:cycle % len(status)] + status[cycle % len(status)].upper() + status[cycle % len(
                        status) + 1:]
                elif status[cycle % len(status)] in list(string.ascii_uppercase):
                    status = status[:cycle % len(status)] + status[cycle % len(status)].lower() + status[cycle % len(
                        status) + 1:]
                sys.stdout.write(self.badges.P + status)
                time.sleep(.1)
                sys.stdout.flush()
        loading_process.join()
