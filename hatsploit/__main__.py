"""
MIT License

Copyright (c) 2020-2023 EntySec

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import argparse
import os
import sys
import yaml

from hatsploit.core.base.console import Console
from hatsploit.core.cli.badges import Badges
from hatsploit.core.db.builder import Builder
from hatsploit.core.utils.api import API
from hatsploit.core.utils.check import Check
from hatsploit.core.utils.update import Update
from hatsploit.lib.config import Config
from hatsploit.lib.jobs import Jobs
from hatsploit.lib.runtime import Runtime


class HatSploit(object):
    """ Main class of hatsploit module.

    This main class of hatsploit module is a representation of
    HatSploit Framework CLI interface.
    """

    def __init__(self) -> None:
        super().__init__()

        self.jobs = Jobs()
        self.config = Config()
        self.runtime = Runtime()

        self.console = Console()
        self.builder = Builder()
        self.badges = Badges()
        self.check = Check()
        self.update = Update()

        self.path_config = self.config.path_config

    def policy(self) -> bool:
        """ Print Terms of Service and ask for confirmation.

        :return bool: True if user accepted Terms of Service
        else False
        """

        if not os.path.exists(self.path_config['accept_path']):
            self.badges.print_information("--( The HatSploit Terms of Service )--")

            with open(
                    self.path_config['policy_path'] + 'terms_of_service.txt', 'r'
            ) as f:
                self.badges.print_empty(f.read())

            agree = self.badges.input_question(
                "Accept HatSploit Framework Terms of Service? [y/n] "
            )
            if agree[0].lower() not in ['y', 'yes']:
                return False

            open(self.path_config['accept_path'], 'w').close()

        return True

    def launch(self, shell: bool = True, scripts: list = []) -> None:
        """ Launch HatSploit CLI interpreter.

        :param bool shell: True to launch shell interpreter
        after all scripts executed else False
        :param list scripts: list of filenames of files
        containing HatSploit scripts
        :return None: None
        """

        if self.runtime.catch(self.runtime.check) is not Exception:
            if self.policy():
                build = False

                if not self.builder.check_base_built():
                    build = self.badges.input_question(
                        "Do you want to build and connect base databases? [y/n] "
                    )
                    build = build[0].lower() in ['y', 'yes']

                if self.runtime.catch(self.runtime.start, [build]) is not Exception:
                    if not scripts:
                        if shell:
                            self.console.shell()
                    else:
                        self.console.script(scripts, shell)

    def cli(self) -> None:
        """ Main command-line arguments handler.

        :return None: None
        """

        description = "Modular penetration testing platform that enables you to write, test, and execute exploit code."
        parser = argparse.ArgumentParser(description=description)
        parser.add_argument(
            '-c',
            '--check',
            dest='check_all',
            action='store_true',
            help='Check base modules, payloads, encoders and plugins.',
        )
        parser.add_argument(
            '--check-modules',
            dest='check_modules',
            action='store_true',
            help='Check only base modules.',
        )
        parser.add_argument(
            '--check-payloads',
            dest='check_payloads',
            action='store_true',
            help='Check only base payloads.',
        )
        parser.add_argument(
            '--check-encoders',
            dest='check_encoders',
            action='store_true',
            help='Check only base encoders.',
        )
        parser.add_argument(
            '--check-plugins',
            dest='check_plugins',
            action='store_true',
            help='Check only base plugins.',
        )
        parser.add_argument(
            '--rest-api',
            dest='rest_api',
            action='store_true',
            help='Start HatSploit REST API server.',
        )
        parser.add_argument(
            '--host',
            dest='host',
            help='HatSploit REST API server host. [default: 127.0.0.1]',
        )
        parser.add_argument(
            '--port',
            dest='port',
            type=int,
            help='HatSploit REST API server port. [default: 8008]',
        )
        parser.add_argument(
            '--username', dest='username', help='HatSploit REST API server username.'
        )
        parser.add_argument(
            '--password', dest='password', help='HatSploit REST API server password.'
        )
        parser.add_argument(
            '-u',
            '--update',
            dest='update',
            action='store_true',
            help='Update HatSploit Framework.',
        )
        parser.add_argument(
            '-s',
            '--script',
            dest='script',
            help='Execute HatSploit commands from script file.',
        )
        parser.add_argument(
            '--no-exit',
            dest='no_exit',
            action='store_true',
            help='Do not exit after script execution.',
        )
        parser.add_argument(
            '--no-startup',
            dest='no_startup',
            action='store_true',
            help='Do not execute startup.hsf file.',
        )
        args = parser.parse_args()

        if args.check_all:
            sys.exit(not self.check.check_all())

        elif args.check_modules:
            sys.exit(self.check.check_modules())

        elif args.check_payloads:
            sys.exit(self.check.check_payloads())

        elif args.check_plugins:
            sys.exit(self.check.check_plugins())

        elif args.check_encoders:
            sys.exit(self.check.check_encoders())

        elif args.rest_api:
            if not args.username and not args.password:
                parser.print_help()
                sys.exit(1)
            else:
                host, port = '127.0.0.1', 8008
                if args.host:
                    host = args.host

                if args.port:
                    port = args.port

                rest_api = API(
                    host=host, port=port, username=args.username, password=args.password
                )

                self.jobs.create_job(
                    f"REST API on port {str(port)}", "", rest_api.run
                )

        elif args.update:
            self.update.update()
            sys.exit(0)

        elif args.script:
            if not os.path.exists(args.script):
                hsf.badges.print_error(f"Local file: {args.script}: does not exist!")
                sys.exit(1)

            if args.no_startup:
                self.launch(shell=args.no_exit, scripts=[args.script])

            else:
                if os.path.exists(self.path_config['startup_path']):
                    self.launch(
                        shell=args.no_exit,
                        scripts=[self.path_config['startup_path'], args.script],
                    )

            sys.exit(0)

        if args.no_startup:
            self.launch()
        else:
            if os.path.exists(self.path_config['startup_path']):
                self.launch(scripts=[self.path_config['startup_path']])
            else:
                self.launch()
