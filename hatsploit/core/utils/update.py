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
import requests
import shutil
import subprocess

from packaging import version
from badges import Badges

from hatsploit.lib.config import Config


class Update(object):
    """ Subclass of hatsploit.core.utils module.

    This subclass of hatsploit.core.utils module is intended for
    providing tools for working with HatSploit updates.
    """

    def __init__(self) -> None:
        super().__init__()

        self.config = Config()
        self.badges = Badges()

    def check_update(self) -> bool:
        """ Check for HatSploit update.

        :return bool: True if update available else False
        """

        try:
            remote_config = requests.get(
                'https://raw.githubusercontent.com/EntySec/HatSploit/main/hatsploit/config/core_config.yml',
                stream=True,
            ).content

        except Exception:
            remote_config = None

        if remote_config:
            remote_version = self.config.get_config_file(remote_config)['details'][
                'version'
            ]
            local_version = self.config.core_config['details']['version']

            return version.parse(local_version) < version.parse(remote_version)
        return False

    def update(self) -> None:
        """ Check for HatSploit update and update it if update
        is available.

        :return None: None
        """

        if self.check_update():
            self.badges.print_process("Updating HatSploit Framework...")
            shutil.rmtree(os.path.abspath(self.config.path_config['root_path']))

            subprocess.call(
                [
                    'pip3',
                    'install',
                    'git+https://github.com/EntySec/HatSploit',
                    '--ignore-installed',
                ],
                shell=False,
            )

            self.badges.print_success("HatSploit updated successfully!")
            return

        self.badges.print_warning("Your HatSploit is up-to-date.")
