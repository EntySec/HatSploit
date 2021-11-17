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

from hatsploit.lib.config import Config

config = Config()
config.configure()

from hatsploit.lib.jobs import Jobs

from hatsploit.core.base.console import Console
from hatsploit.core.cli.badges import Badges
from hatsploit.core.utils.check import Check
from hatsploit.core.utils.update import Update
from hatsploit.core.utils.api import API


class HatSploit:
    jobs = Jobs()
    console = Console()
    badges = Badges()
    check = Check()
    update = Update()
    api = API()

    root_path = config.path_config['root_path']

    def accept_terms_of_service(self):
        if not os.path.exists(self.root_path + '.accepted'):
            self.badges.print_information("--( The HatSploit Terms of Service )--")
            terms = """
This tool is designed for educational purposes only.

Adequate defenses can only be built by researching attack techniques available to malicious actors.
Using this tool against target systems without prior permission is illegal in most jurisdictions.
The authors are not liable for any damages from misuse of this information or code.

If you are planning on using this tool for malicious purposes that are not authorized by the company
you are performing assessments for, you are violating the terms of service and license. 

By accepting our terms of service, you agree that you will only use this tool for lawful purposes only.
"""

            self.badges.print_empty(terms)

            agree = self.badges.input_question("Accept HatSploit Framework Terms of Service? [y/n] ")
            if agree[0].lower() not in ['y', 'yes']:
                return False

            open(self.root_path + '.accepted', 'w').close()
            return True
        return True

    def launch(self, do_shell=True, script=[]):
        if self.console.check_install():
            if self.accept_terms_of_service():
                if not script:
                    if do_shell:
                        self.console.shell()
                else:
                    self.console.script(script, do_shell)


def main():
    description = "Modular penetration testing platform that enables you to write, test, and execute exploit code."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-c', '--check', dest='check_all', action='store_true',
                        help='Check base modules, payloads and plugins.')
    parser.add_argument('--check-modules', dest='check_modules', action='store_true', help='Check only base modules.')
    parser.add_argument('--check-payloads', dest='check_payloads', action='store_true',
                        help='Check only base payloads.')
    parser.add_argument('--check-plugins', dest='check_plugins', action='store_true', help='Check only base plugins.')
    parser.add_argument('-u', '--update', dest='update', action='store_true', help='Update HatSploit Framework.')
    parser.add_argument('--rest-api', dest='rest_api', action='store_true', help='Run HatSploit with REST API.')
    parser.add_argument('--port', dest='port', type=int, help='HatSploit REST API port. [default: 8008]')
    parser.add_argument('-s', '--script', dest='script', help='Execute HatSploit commands from script file.')
    parser.add_argument('--no-exit', dest='no_exit', action='store_true', help='Do not exit after script execution.')
    parser.add_argument('--no-startup', dest='no_startup', action='store_true', help='Do not execute startup.hsf file.')
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
    elif args.update:
        hsf.update.update()
    elif args.rest_api:
        if args.port:
            hsf.jobs.create_job(
                "HatSploit REST API",
                None,
                hsf.api.init,
                [args.port],
                True
            )
        else:
            hsf.jobs.create_job(
                "HatSploit REST API",
                None,
                hsf.api.init,
                hidden=True
            )
    elif args.script:
        if not os.path.exists(args.script):
            hsf.badges.print_error(f"Local file: {args.script}: does not exist!")
            sys.exit(1)
        if args.no_startup:
            hsf.launch(
                do_shell=args.no_exit,
                script=[args.script]
            )
        else:
            if os.path.exists(hsf.root_path + 'startup.hsf'):
                hsf.launch(
                    do_shell=args.no_exit,
                    script=[hsf.root_path + 'startup.hsf', args.script]
                )
        sys.exit(0)
    if args.no_startup:
        hsf.launch()
    else:
        if os.path.exists(hsf.root_path + 'startup.hsf'):
            hsf.launch(
                script=[hsf.root_path + 'startup.hsf']
            )
        else:
            hsf.launch()
