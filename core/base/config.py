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

import yaml

from core.cli.badges import badges
from core.base.storage import local_storage
from core.base.storage import global_storage

class config:
    def __init__(self):
        self.badges = badges()
        self.local_storage = local_storage()
        
        self.base_path = '/opt/hsf/'
        self.config_path = self.base_path + 'config/'
        
        self.db_config_file = self.config_path + 'db_config.yml'
        self.path_config_file = self.config_path + 'path_config.yml'
        self.core_config_file = self.config_path + 'core_config.yml'
        
        self.db_config = self.local_storage.get("db_config")
        self.path_config = self.local_storage.get("path_config")
        self.core_config = self.local_storage.get("core_config")

    def get_config_file(self, content):
        return yaml.safe_load(content)
        
    def configure(self):
        db_config = self.get_config_file(open(self.db_config_file))
        path_config = self.get_config_file(open(self.path_config_file))
        core_config = self.get_config_file(open(self.core_config_file))

        self.db_config = db_config
        self.path_config = path_config
        self.core_config = core_config
        
        self.local_storage.set("db_config", self.db_config)
        self.local_storage.set("path_config", self.path_config)
        self.local_storage.set("core_config", self.core_config)
        
        self.global_storage = global_storage(self.path_config['base_paths']['storage_path'])
        self.global_storage.set_all()
