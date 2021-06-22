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
import string
import sys
import threading
import time

from hatsploit.core.base.config import Config
from hatsploit.core.base.exceptions import Exceptions
from hatsploit.core.base.storage import LocalStorage
from hatsploit.core.cli.badges import Badges
from hatsploit.core.db.db import DB


class Importer:
    def __init__(self):
        self.db = DB()
        self.badges = Badges()
        self.local_storage = LocalStorage()
        self.config = Config()
        self.exceptions = Exceptions()

    def get_module(self, mu, name, folderpath):
        folderpath_list = folderpath.split(".")
        for i in dir(mu):
            if i == name:
                return getattr(mu, name)
            if i in folderpath_list:
                i = getattr(mu, i)
                return self.get_module(i, name, folderpath)
        return None

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
            command_directory = command_path
            command_file = os.path.split(command_directory)[1]
            command_directory = command_directory.replace('/', '.')
            command_object = __import__(command_directory)
            command_object = self.get_module(command_object, command_file, command_directory)
            command_object = command_object.HatSploitCommand()
        except Exception as e:
            self.badges.output_information('Reason: ' + str(e))
            raise self.exceptions.GlobalException
        return command_object

    def import_payload(self, payload_path):
        try:
            payload_directory = payload_path
            payload_file = os.path.split(payload_directory)[1]
            payload_directory = payload_directory.replace('/', '.')
            payload_object = __import__(payload_directory)
            payload_object = self.get_module(payload_object, payload_file, payload_directory)
            payload_object = payload_object.HatSploitPayload()
        except Exception as e:
            self.badges.output_information('Reason: ' + str(e))
            raise self.exceptions.GlobalException
        return payload_object

    def import_module(self, module_path):
        try:
            module_directory = module_path
            module_file = os.path.split(module_directory)[1]
            module_directory = module_directory.replace('/', '.')
            module_object = __import__(module_directory)
            module_object = self.get_module(module_object, module_file, module_directory)
            module_object = module_object.HatSploitModule()
        except Exception as e:
            self.badges.output_information('Reason: ' + str(e))
            raise self.exceptions.GlobalException
        return module_object

    def import_plugin(self, plugin_path):
        try:
            plugin_directory = plugin_path
            plugin_file = os.path.split(plugin_directory)[1]
            plugin_directory = plugin_directory.replace('/', '.')
            plugin_object = __import__(plugin_directory)
            plugin_object = self.get_module(plugin_object, plugin_file, plugin_directory)
            plugin_object = plugin_object.HatSploitPlugin()
        except Exception as e:
            self.badges.output_information('Reason: ' + str(e))
            raise self.exceptions.GlobalException
        return plugin_object

    def import_commands(self):
        commands = dict()
        command_path = self.config.path_config['base_paths']['commands_path']
        try:
            for file in os.listdir(command_path):
                if file.endswith('py'):
                    command_file_path = command_path + file[:-3]
                    command_directory = command_file_path.replace(self.config.path_config['base_paths']['root_path'],
                                                                  '', 1)
                    try:
                        command_object = self.import_command(command_directory)
                        command_name = command_object.details['Name']
                        commands[command_name] = command_object
                        self.local_storage.set("commands", commands)
                    except Exception:
                        self.badges.output_error("Failed to load " + file[:-3] + " command!")
        except Exception:
            pass

    def import_database(self):
        self.db.connect_modules_database('hsf_modules', self.config.path_config['base_paths']['db_path'] +
                                         self.config.db_config['base_dbs']['modules_database'])
        self.db.connect_payloads_database('hsf_payloads', self.config.path_config['base_paths']['db_path'] +
                                          self.config.db_config['base_dbs']['payloads_database'])
        self.db.connect_plugins_database('hsf_plugins', self.config.path_config['base_paths']['db_path'] +
                                         self.config.db_config['base_dbs']['plugins_database'])

    def import_all(self, import_database):
        self.import_commands()
        if import_database:
            self.import_database()
