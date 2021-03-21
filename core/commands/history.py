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

import readline

from core.base.config import Config
from core.base.storage import GlobalStorage
from core.base.storage import LocalStorage
from core.lib.command import Command


class HatSploitCommand(Command):
    config = Config()
    local_storage = LocalStorage()

    history = config.path_config['base_paths']['history_path']
    storage_path = config.path_config['base_paths']['storage_path']

    global_storage = GlobalStorage(storage_path)

    usage = ""
    usage += "history <option>\n\n"
    usage += "  -l, --list   List all history.\n"
    usage += "  -c, --clear  Clear all history.\n"
    usage += "  on/off       Turn history on/off.\n"

    details = {
        'Category': "developer",
        'Name': "history",
        'Authors': [
            'enty8080'
        ],
        'Description': "Manage HatSploit history.",
        'Usage': usage,
        'MinArgs': 1
    }

    def run(self, argc, argv):
        option = argv[0]
        if option == "on":
            self.local_storage.set("history", True)
            self.global_storage.set("history", True)
            self.output_information("HatSploit history: on")
        elif option == "off":
            self.local_storage.set("history", False)
            self.global_storage.set("history", False)
            self.output_information("HatSploit history: off")
        elif option in ['-c', '--clear']:
            readline.clear_history()
            with open(self.history, 'w') as history:
                history.write("")
        elif option in ['-l', '--list']:
            using_history = self.local_storage.get("history")
            if using_history:
                if readline.get_current_history_length() > 0:
                    self.output_information("HatSploit history:")

                    history_file = open(self.history, 'r')
                    history = [x.strip() for x in history_file.readlines()]
                    history_file.close()
                    for line in history:
                        self.output_empty("    * " + line)

                    for index in range(1, readline.get_current_history_length()):
                        self.output_empty("    * " + readline.get_history_item(index))
                else:
                    self.output_warning("HatSploit history empty.")
            else:
                self.output_warning("No history detected.")
        else:
            self.output_usage(self.details['Usage'])
