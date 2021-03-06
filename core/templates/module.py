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

from core.cli.badges import badges
from core.cli.parser import parser
from core.cli.tables import tables

from core.base.jobs import jobs
from core.base.config import config
from core.base.sessions import sessions
from core.base.exceptions import exceptions
from core.base.storage import local_storage
from core.base.storage import global_storage

from core.modules.modules import modules

from utils.adb_tools import adb_tools
from utils.fsmanip import fsmanip
from utils.hatvenom import hatvenom
from utils.web_tools import web_tools
from utils.tcp_tools import tcp_tools
from utils.pseudo_shell import pseudo_shell
from utils.string_tools import string_tools

class HatSploitModule():
    def __init__(self):
        self.badges = badges()
        self.parser = parser()
        self.tables = tables()
        
        self.jobs = jobs()
        self.config = config()
        self.sessions = sessions()
        self.exceptions = exceptions()
        self.local_storage = local_storage()
        self.global_storage = global_storage()
        
        self.modules = modules()
        
        self.adb_tools = adb_tools()
        self.fsmanip = fsmanip()
        self.hatvenom = hatvenom()
        self.web_tools = web_tools()
        self.tcp_tools = tcp_tools()
        self.pseudo_shell = pseudo_shell()
        self.string_tools = string_tools()
        
        self.details = {
            'Name': "",
            'Module': "",
            'Authors': [
                ''
            ],
            'Description': "",
            'Dependencies': [
                ''
            ],
            'Comments': [
                ''
            ],
            'Risk': ""
        }
        
        self.options = {
            '': {
                'Description': "",
                'Value': None,
                'Required': True
            }
        }

        self.commands = {
            '': {
                'Description': "",
                'Usage': "",
                'MinArgs': 0,
                'Run': self.command
            }
        }

    def command(self, argc, argv):
        pass
        
    def run(self):
        pass
