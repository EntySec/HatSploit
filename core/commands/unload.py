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

from core.base.storage import LocalStorage
from core.lib.command import Command
from core.plugins.plugins import Plugins


class HatSploitCommand(Command):
    local_storage = LocalStorage()
    plugins = Plugins()

    details = {
        'Category': "plugin",
        'Name': "unload",
        'Authors': [
            'Ivan Nikolsky (enty8080)'
        ],
        'Description': "Unload specified loaded plugin.",
        'Usage': "unload <plugin>",
        'MinArgs': 1
    }

    def run(self, argc, argv):
        plugin = argv[0]
        self.output_process("Unloading " + plugin + " plugin...")

        if self.plugins.check_loaded(plugin):
            self.local_storage.delete_element("loaded_plugins", plugin)
            self.output_success("Successfully unloaded " + plugin + " plugin!")
        else:
            self.output_error("Plugin not loaded!")
