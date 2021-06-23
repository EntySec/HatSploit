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

import sys

sys.stdout.write("\033]0;HatSploit Framework\007")

import os
import yaml
import argparse

from hatsploit.core.base.config import Config

config = Config()
config.configure()

from hatsploit.core.base.console import Console
from hatsploit.core.cli.badges import Badges
from hatsploit.core.utils.check import Check


class HatSploit:
    def __init__(self):
        self.console = Console()
        self.badges = Badges()
        self.check = Check()

        self.root_path = config.path_config['base_paths']['root_path']

    def accept_terms_of_service(self):
        if not os.path.exists(self.root_path + '.accepted'):
            self.badges.output_information("--( The HatSploit Terms of Service )--\n")

            file = open(self.root_path + 'TERMS_OF_SERVICE.md', 'r')
            terms = file.read()
            file.close()

            self.badges.output_empty(terms)

            agree = self.badges.input_question("Accept HatSploit Framework Terms of Service? [y/n] ")
            if agree.lower() not in ['y', 'yes']:
                return False

            open(self.root_path + '.accepted', 'w').close()
            return True
        return True

    def launch(self):
        if self.console.check_install():
            if self.accept_terms_of_service():
                self.console.shell()

def main():
    description = "Modular penetration testing platform that enables you to write, test, and execute exploit code."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-c', '--check', dest='check_all', action='store_true', help='Check stdalone modules, payloads and plugins.')
    parser.add_argument('--check-modules', dest='check_modules', action='store_true', help='Check only stdalone modules.')
    parser.add_argument('--check-payloads', dest='check_payloads', action='store_true', help='Check only stdalone payloads.')
    parser.add_argument('--check-plugins', dest='check_plugins', action='store_true', help='Check only stdalone plugins.')
    args = parser.parse_args()

    hsf = HatSploit()

    if args.check_all:
        if not hsf.check.check_all():
            sys.exit(0)
    elif args.check_modules:
        if not hsf.check.check_modules():
            sys.exit(0)
    elif args.check_payloads:
        if not hsf.check.check_payloads():
            sys.exit(0)
    elif args.check_plugins:
        if hsf.check.check_plugins():
            sys.exit(0)
    else:
        hsf.launch()
