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

import importlib.util
import json
import os
import string
import sys
import threading
import time

from hatsploit.core.base.exceptions import Exceptions
from hatsploit.core.cli.badges import Badges
from hatsploit.core.db.db import DB
from hatsploit.lib.config import Config
from hatsploit.lib.storage import LocalStorage


class Importer:
    db = DB()
    badges = Badges()
    local_storage = LocalStorage()
    config = Config()
    exceptions = Exceptions()

    @staticmethod
    def import_check(module_name):
        try:
            __import__(module_name)
        except ModuleNotFoundError:
            return False
        except Exception:
            return True
        return True

    def import_command(self, command_path):
        try:
            if not command_path.endswith('.py'):
                command_path = command_path + '.py'
            spec = importlib.util.spec_from_file_location(command_path, command_path)
            command = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(command)
            command = command.HatSploitCommand()
        except Exception as e:
            self.badges.print_information('Reason: ' + str(e))
            raise self.exceptions.GlobalException
        return command

    def import_payload(self, payload_path):
        try:
            if not payload_path.endswith('.py'):
                payload_path = payload_path + '.py'
            spec = importlib.util.spec_from_file_location(payload_path, payload_path)
            payload = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(payload)
            payload = payload.HatSploitPayload()
        except Exception as e:
            self.badges.print_information('Reason: ' + str(e))
            raise self.exceptions.GlobalException
        return payload

    def import_module(self, module_path):
        try:
            if not module_path.endswith('.py'):
                module_path = module_path + '.py'
            spec = importlib.util.spec_from_file_location(module_path, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            module = module.HatSploitModule()
        except Exception as e:
            self.badges.print_information('Reason: ' + str(e))
            raise self.exceptions.GlobalException
        return module

    def import_plugin(self, plugin_path):
        try:
            if not plugin_path.endswith('.py'):
                plugin_path = plugin_path + '.py'
            spec = importlib.util.spec_from_file_location(plugin_path, plugin_path)
            plugin = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(plugin)
            plugin = plugin.HatSploitPlugin()
        except Exception as e:
            self.badges.print_information('Reason: ' + str(e))
            raise self.exceptions.GlobalException
        return plugin

    def import_commands(self):
        commands = dict()
        command_path = os.path.split(
            self.config.path_config['commands_path']
        )[0]
        try:
            for file in os.listdir(command_path):
                if file.endswith('py'):
                    try:
                        command_object = self.import_command(command_path + '/' + file[:-3])
                        command_name = command_object.details['Name']
                        commands[command_name] = command_object
                        self.local_storage.set("commands", commands)
                    except Exception:
                        self.badges.print_error("Failed to load " + file[:-3] + " command!")
        except Exception:
            pass

    def import_database(self):
        self.db.connect_modules_database(self.config.db_config['base_dbs']['modules_database_name'],
                                         self.config.path_config['db_path'] + self.config.db_config['base_dbs'][
                                             'modules_database'])
        self.db.connect_payloads_database(self.config.db_config['base_dbs']['payloads_database_name'],
                                          self.config.path_config['db_path'] + self.config.db_config['base_dbs'][
                                              'payloads_database'])
        self.db.connect_plugins_database(self.config.db_config['base_dbs']['plugins_database_name'],
                                         self.config.path_config['db_path'] + self.config.db_config['base_dbs'][
                                             'plugins_database'])

    def import_all(self, import_database):
        self.import_commands()
        if import_database:
            self.import_database()
