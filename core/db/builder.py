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

import json
import os

from core.modules.modules import Modules
from core.payloads.payloads import Payloads
from core.base.config import Config
from core.db.importer import Importer
from core.base.storage import LocalStorage
from core.cli.badges import Badges


class Builder:
    def __init__(self):
        self.modules = Modules()
        self.payloads = Payloads()
        self.badges = Badges()
        self.config = Config()
        self.importer = Importer()
        self.local_storage = LocalStorage()

    def check_built(self):
        if os.path.exists(self.config.path_config['base_paths']['db_path'] +
                        self.config.db_config['base_dbs']['modules_database']) and
        os.path.exists(self.config.path_config['base_paths']['db_path'] +
                        self.config.db_config['base_dbs']['payloads_database']) and
        os.path.exists(self.config.path_config['base_paths']['db_path'] +
                        self.config.db_config['base_dbs']['plugins_database']):
            return True
        return False

    def build_payloads_database(self):
        self.badges.output_process("Building stdalone payloads database...")
        database_path = self.config.path_config['base_paths']['db_path'] +
                        self.config.db_config['base_dbs']['payloads_database']
        database = {
            "__database__": {
                "type": "payloads"
            }
        }

        payloads_path = 'payloads'
        for dest, _, files in os.walk(payloads_path):
            for file in files:
                if file.endswith('.py') and file != '__init__.py':
                    payload = dest + '/' + file[:-3]
                    payload_object = self.importer.import_payload(payload)

                    database.update({
                        self.payloads.get_platform(payload): {
                            self.payloads.get_architecture(payload): {
                                self.payloads.get_name(payload): {
                                    "Path": payload,
                                    "Category": payload_object.details['Category'],
                                    "Name": payload_object.details['Name'],
                                    "Payload": payload_object.details['Payload'],
                                    "Authors": payload_object.details['Authors'],
                                    "Description": payload_object.details['Description'],
                                    "Comments": payload_object.details['Comments'],
                                    "Architecture": payload_object.details['Architecture'],
                                    "Platform": payload_object.details['Platform'],
                                    "Risk": payload_object.details['Risk'],
                                    "Type": payload_object.details['Type']
                                }
                            }
                        }
                    })

        with open('database_path', 'w') as f:
            json.dump(database, f)

    def build_modules_database(self):
        self.badges.output_process("Building stdalone modules database...")
        database_path = self.config.path_config['base_paths']['db_path'] +
                        self.config.db_config['base_dbs']['modules_database']
        database = {
            "__database__": {
                "type": "modules"
            }
        }

        modules_path = 'modules'
        for dest, _, files in os.walk(modules_path):
            for file in files:
                if file.endswith('.py') and file != '__init__.py':
                    module = dest + '/' + file[:-3]
                    module_object = self.importer.import_module(module)

                    database.update({
                        self.modules.get_category(module): {
                            self.modules.get_platform(module): {
                                self.modules.get_name(module): {
                                    "Path": module,
                                    "Name": module_object.details['Name'],
                                    "Module": module_object.details['Module'],
                                    "Authors": module_object.details['Authors'],
                                    "Description": module_object.details['Description'],
                                    "Comments": module_object.details['Comments'],
                                    "Platform": module_object.details['Platform'],
                                    "Risk": module_object.details['Risk']
                                }
                            }
                        }
                    })

        with open('database_path', 'w') as f:
            json.dump(database, f)

    def build_plugins_database(self):
        self.badges.output_process("Building stdalone plugins database...")
        database_path = self.config.path_config['base_paths']['db_path'] +
                        self.config.db_config['base_dbs']['plugins_database']
        database = {
            "__database__": {
                "type": "plugins"
            }
        }

        plugins_path = 'plugins'
        for dest, _, files in os.walk(plugins_path):
            for file in files:
                if file.endswith('.py') and file != '__init__.py':
                    plugin = dest + '/' + file[:-3]
                    plugin_object = self.importer.import_plugin(plugin)

                    database.update({
                        plugin.strip(plugins_path + '/'): {
                            "Path": plugin,
                            "Name": plugin_object.details['Name'],
                            "Authors": plugin_object.details['Authors'],
                            "Description": plugin_object.details['Description'],
                            "Comments": plugin_object.details['Comments']
                        }
                    })

        with open('database_path', 'w') as f:
            json.dump(database, f)
