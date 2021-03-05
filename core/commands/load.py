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

from core.cli.badges import badges
from core.base.storage import local_storage
from core.plugins.plugins import plugins
from core.db.importer import importer

class HatSploitCommand:
    def __init__(self):
        self.badges = badges()
        self.local_storage = local_storage()
        self.plugins = plugins()
        self.importer = importer()

        self.details = {
            'Category': "plugin",
            'Name': "load",
            'Description': "Load specified plugin.",
            'Usage': "load <plugin>",
            'MinArgs': 1
        }

    def import_plugin(self, database, plugin):
        loaded_plugins = dict()
        plugins = self.local_storage.get("plugins")[database][plugin]
        try:
            loaded_plugins[plugin] = self.importer.import_plugin(plugins['Path'])
        except Exception:
            return None
        return loaded_plugins
        
    def add_plugin(self, database, plugin):
        plugins = self.local_storage.get("plugins")[database][plugin]
        not_installed = list()
        for dependence in plugins['Dependencies']:
            if not self.importer.import_check(dependence):
                not_installed.append(dependence)
        if not not_installed:
            plugin_object = self.import_plugin(database, plugin)
            if plugin_object:
                if self.local_storage.get("loaded_plugins"):
                    self.local_storage.update("loaded_plugins", plugin_object)
                else:
                    self.local_storage.set("loaded_plugins", plugin_object)
                self.local_storage.get("loaded_plugins")[plugin].run()
                self.badges.output_success("Successfully loaded " + plugin + " plugin!")
            else:
                self.badges.output_error("Failed to load plugin!")
        else:
            self.badges.output_error("Plugin depends this dependencies which is not installed:")
            for dependence in not_installed:
                self.badges.output_empty("    * " + dependence)
        
    def run(self, argc, argv):
        plugin = argv[0]
        self.badges.output_process("Loading " + plugin + " plugin...")
        
        if not self.plugins.check_loaded(plugin):
            if self.plugins.check_exist(plugin):
                database = self.plugins.get_database(plugin)
                self.add_plugin(database, plugin)
            else:
                self.badges.output_error("Invalid plugin!")
        else:
            self.badges.output_error("Already loaded!")
