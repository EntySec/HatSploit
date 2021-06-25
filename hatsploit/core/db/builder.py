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

import collections
import json
import os

from hatsploit.base.modules import Modules
from hatsploit.base.payloads import Payloads
from hatsploit.base.config import Config
from hatsploit.core.db.importer import Importer
from hatsploit.base.storage import LocalStorage
from hatsploit.core.cli.badges import Badges


class Builder:
    def __init__(self):
        self.modules = Modules()
        self.payloads = Payloads()
        self.badges = Badges()
        self.config = Config()
        self.importer = Importer()
        self.local_storage = LocalStorage()

    def check_base_built(self):
        if (os.path.exists(self.config.path_config['db_path'] +
                        self.config.db_config['base_dbs']['modules_database']) and
        os.path.exists(self.config.path_config['db_path'] +
                        self.config.db_config['base_dbs']['payloads_database']) and
        os.path.exists(self.config.path_config['db_path'] +
                        self.config.db_config['base_dbs']['plugins_database'])):
            return True
        return False

    def build_base(self):
        if not self.check_stdalone_built():
            if not os.path.exists(self.config.path_config['db_path']):
                os.mkdir(self.config.path_config['db_path'])

            self.build_modules_database(self.config.path_config['modules_path'],
                                        (self.config.path_config['db_path'] + 
                                         self.config.db_config['base_dbs']['modules_database']))
            self.build_payloads_database(self.config.path_config['payloads_path'],
                                        (self.config.path_config['db_path'] + 
                                         self.config.db_config['base_dbs']['payloads_database']))
            self.build_plugins_database(self.config.path_config['plugins_path'],
                                        (self.config.path_config['db_path'] + 
                                         self.config.db_config['base_dbs']['plugins_database']))

    def recursive_update(self, d, u):
        for k, v in u.items():
            if isinstance(d, collections.abc.Mapping):
                if isinstance(v, collections.abc.Mapping):
                    r = self.recursive_update(d.get(k, {}), v)
                    d[k] = r
                else:
                    d[k] = u[k]
            else:
                d = {k: u[k]}
        return d

    def build_payloads_database(self, input_path, output_path):
        database_path = output_path
        database = {
            "__database__": {
                "type": "payloads"
            }
        }

        payloads_path = os.path.normpath(input_path)
        for dest, _, files in os.walk(payloads_path):
            for file in files:
                if file.endswith('.py') and file != '__init__.py':
                    payload = dest + '/' + file[:-3]
                    payload_name = payload[len(f"{payloads_path}/"):]

                    try:
                        payload_object = self.importer.import_payload(payload)
                        self.recursive_update(database, {
                            self.payloads.get_platform(payload_name): {
                                self.payloads.get_architecture(payload_name): {
                                    self.payloads.get_name(payload_name): {
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
                    except Exception:
                        self.badges.output_error(f"Failed to add {payload_name} to payloads database!")

        with open(database_path, 'w') as f:
            json.dump(database, f)

    def build_modules_database(self, input_path, output_path):
        database_path = output_path
        database = {
            "__database__": {
                "type": "modules"
            }
        }

        modules_path = os.path.normpath(input_path)
        for dest, _, files in os.walk(modules_path):
            for file in files:
                if file.endswith('.py') and file != '__init__.py':
                    module = dest + '/' + file[:-3]
                    module_name = module[len(f"{modules_path}/"):]

                    try:
                        module_object = self.importer.import_module(module)
                        self.recursive_update(database, {
                            self.modules.get_category(module_name): {
                                self.modules.get_platform(module_name): {
                                    self.modules.get_name(module_name): {
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
                    except Exception:
                        self.badges.output_error(f"Failed to add {module_name} to modules database!")

        with open(database_path, 'w') as f:
            json.dump(database, f)

    def build_plugins_database(self, input_path, output_path):
        database_path = output_path
        database = {
            "__database__": {
                "type": "plugins"
            }
        }

        plugins_path = os.path.normpath(input_path)
        for dest, _, files in os.walk(plugins_path):
            for file in files:
                if file.endswith('.py') and file != '__init__.py':
                    plugin = dest + '/' + file[:-3]
                    plugin_name = plugin[len(f"{plugins_path}/"):]

                    try:
                        plugin_object = self.importer.import_plugin(plugin)
                        self.recursive_update(database, {
                            plugin_name: {
                                "Path": plugin,
                                "Name": plugin_object.details['Name'],
                                "Authors": plugin_object.details['Authors'],
                                "Description": plugin_object.details['Description'],
                                "Comments": plugin_object.details['Comments']
                            }
                        })
                    except Exception:
                        self.badges.output_error(f"Failed to add {plugin_name} to plugins database!")

        with open(database_path, 'w') as f:
            json.dump(database, f)
