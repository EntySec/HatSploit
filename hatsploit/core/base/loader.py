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

import string
import threading
import time

from badges import Badges

from hatsploit.core.db.builder import Builder
from hatsploit.core.db.importer import Importer
from hatsploit.core.utils.update import Update

from hatsploit.lib.config import Config


class Loader(object):
    """ Subclass of hatsploit.core.base module.

    This subclass of hatsploit.core.base module is intended
    for providing HatSploit loader.
    """

    def __init__(self) -> None:
        super().__init__()

        self.badges = Badges()
        self.importer = Importer()
        self.builder = Builder()
        self.update = Update()

        self.config = Config()

    def load_update_process(self) -> None:
        """ Check for update and notify user if one available.

        :return None: None
        """

        if self.update.check_update():
            self.badges.print_warning("Your HatSploit Framework is out-dated.")
            self.badges.print_information("Consider running %greenhsf --update%end.")
            time.sleep(1)

    def load_everything(self, build_base: bool = False) -> None:
        """ Load everything, every single database.

        :param bool build_base: True to build base
        databases else False
        :return None: None
        """

        if build_base:
            self.builder.build_base()

        self.importer.import_all()

    def load_all(self, build_base: bool = False, silent: bool = False) -> None:
        """ Load all: core, databases, interface, etc.

        :param bool build_base: True to build base
        databases else False
        :param bool silent: display loading message if True
        :return None: None
        """

        self.load_update_process()

        if silent:
            self.load_everything(build_base)
            return

        loading_process = threading.Thread(
            target=self.load_everything, args=[build_base]
        )
        loading_process.start()

        base_line = "Loading the HatSploit Framework..."
        cycle = 0

        while loading_process.is_alive():
            for char in r"/-\|":
                status = base_line + char
                cycle += 1

                if status[cycle % len(status)] in list(string.ascii_lowercase):
                    status = (
                            status[: cycle % len(status)]
                            + status[cycle % len(status)].upper()
                            + status[cycle % len(status) + 1:]
                    )

                elif status[cycle % len(status)] in list(string.ascii_uppercase):
                    status = (
                            status[: cycle % len(status)]
                            + status[cycle % len(status)].lower()
                            + status[cycle % len(status) + 1:]
                    )

                self.badges.print_process(status, '', '\r')
                time.sleep(0.1)

        loading_process.join()
