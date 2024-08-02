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

import time
import string
import threading

from hatsploit.core.db.builder import Builder
from hatsploit.core.utils.update import Update


class Loader(Builder):
    """ Subclass of hatsploit.core.base module.

    This subclass of hatsploit.core.base module is intended
    for providing HatSploit loader.
    """

    def load_update_process(self) -> None:
        """ Check for update and notify user if one available.

        :return None: None
        """

        if Update().check_update():
            self.print_warning("Your HatSploit Framework is out-dated.")
            self.print_information("Consider running %greenhsf --update%end.")
            time.sleep(1)

    def load_everything(self, build_base: bool = False) -> None:
        """ Load everything, every single database.

        :param bool build_base: True to build base
        databases else False
        :return None: None
        """

        self.load_update_process()

        if build_base:
            self.build_base()

    def load_all(self, build_base: bool = False, silent: bool = False) -> None:
        """ Load all: core, databases, interface, etc.

        :param bool build_base: True to build base
        databases else False
        :param bool silent: display loading message if True
        :return None: None
        """

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

                self.print_process(status, '', '\r')
                time.sleep(0.1)

        loading_process.join()
