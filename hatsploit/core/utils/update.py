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

import subprocess
import shutil
from packaging import version
import os

import requests

from hatsploit.lib.config import Config
from hatsploit.core.cli.badges import Badges


class Update:
    def __init__(self):
        self.config = Config()
        self.badges = Badges()

    def check_update(self):
        remote_config = requests.get('https://raw.githubusercontent.com/EntySec/HatSploit/main/hatsploit/config/core_config.yml',
                                     stream=True).content
        remote_version = self.config.get_config_file(remote_config)['details']['version']
        local_version = self.config.core_config['details']['version']
        return version.parse(local_version) < version.parse(remote_version)

    def update(self):
        if self.check_update():
            self.badges.output_process("Updating HatSploit Framework...")
            shutil.rmtree(os.path.abspath(self.config.path_config['root_path']))
            subprocess.call(['pip3', 'install', 'git+https://github.com/EntySec/HatSploit', '--ignore-installed'], shell=False)
            self.badges.output_success("HatSploit updated successfully!")
            return
        self.badges.output_warning("Your HatSploit is up-to-date.")
