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

from core.payloads.payloads import Payloads
from core.base.config import Config
from core.db.importer import Importer
from core.base.storage import LocalStorage
from core.cli.badges import Badges


class Builder:
    def __init__(self):
        self.payloads = Payloads()
        self.badges = Badges()
        self.config = Config()
        self.importer = Importer()
        self.local_storage = LocalStorage()

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
                    
                    cache = {
                        self.payloads.get_platform(payload): {
                            self.payloads.get_architecture(payload): {
                                self.payloads.get_name(payload): {
                                    "Path": payload
                                }
                            }
                        }
                    }

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
                    module = dest + '/' + file

    def build_plugins_database(self):
        self.badges.output_process("Building stdalone plugins database...")
        database_path = self.config.path_config['base_paths']['db_path'] +
                        self.config.db_config['base_dbs']['plugins_database']
        database = {
            "__database__": {
                "type": "plugins"
            }
        }

        plugins_path = 'modules'
        for dest, _, files in os.walk(plugins_path):
            for file in files:
                if file.endswith('.py') and file != '__init__.py':
                    plugin = dest + '/' + file
