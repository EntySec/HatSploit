"""
MIT License

Copyright (c) 2020-2024 EntySec

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

from hatasm import HatAsm
from typing import Any, Optional
from badges import Badges, Tables

from pex.platform.types import EXEC_FORMATS

from hatsploit.core.base.console import Console

from hatsploit.core.db.db import DB
from hatsploit.core.db.builder import Builder

from hatsploit.core.utils.rpc import RPC
from hatsploit.core.utils.check import Check
from hatsploit.core.utils.update import Update

from hatsploit.lib.config import Config
from hatsploit.lib.jobs import Jobs
from hatsploit.lib.runtime import Runtime
from hatsploit.lib.payloads import Payloads
from hatsploit.lib.encoders import Encoders
from hatsploit.lib.show import Show


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

    def initialize(self, silent: bool = False) -> bool:
        """ Check build and policy and ask for database.

        :param bool silent: display loading message if True
        :return bool: True if success else False
        """

        if self.runtime.catch(self.runtime.check) is Exception \
                and not self.policy():
            return False

        if not self.policy():
            return False

        build = False

        if not self.builder.check_base_built():
            build = self.badges.input_question(
                "Do you want to build and connect base databases? [y/n] "
            )

            build = build[0].lower() in ['y', 'yes']

        if self.runtime.catch(self.runtime.start, [build, silent]) is Exception:
            return False

        return True

    def launch(self, shell: bool = True, scripts: list = [], rpc: list = []) -> None:
        """ Launch HatSploit CLI interpreter.

        :param bool shell: True to launch shell interpreter
        after all scripts executed else False
        :param list scripts: list of filenames of files
        containing HatSploit scripts
        :param list rpc: RPC host and port
        :return None: None
        """

        if not scripts:
            if shell:
                if len(rpc) >= 2:
                    self.jobs.create_job(f"RPC on port {str(rpc[1])}", "", RPC(*rpc).run)

                self.console.shell()
        else:
            self.console.script(scripts, shell)

    def cli(self) -> None:
        """ Main command-line arguments handler.

        :return None: None
        """

        if not self.initialize():
            return

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
            '--rpc',
            dest='rpc',
            action='store_true',
            help='Start HatSploit RPC server.',
        )
        parser.add_argument(
            '--host',
            dest='host',
            help='HatSploit RPC server host. [default: 127.0.0.1]',
        )
        parser.add_argument(
            '--port',
            dest='port',
            type=int,
            help='HatSploit RPC server port. [default: 5000]',
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

        rpc = ()

        if args.rpc:
            rpc = (args.host or '127.0.0.1', args.port or 5000)

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

        elif args.update:
            self.update.update()
            sys.exit(0)

        elif args.script:
            if not os.path.exists(args.script):
                hsf.badges.print_error(f"Local file: {args.script}: does not exist!")
                sys.exit(1)

            if args.no_startup:
                self.launch(shell=args.no_exit, scripts=[args.script], rpc=rpc)

            else:
                if os.path.exists(self.path_config['startup_path']):
                    self.launch(
                        shell=args.no_exit,
                        scripts=[self.path_config['startup_path'], args.script],
                        rpc=rpc
                    )
                else:
                    self.launch(
                        shell=args.no_exit,
                        scripts=[args.script],
                        rpc=rpc
                    )

            sys.exit(0)

        if args.no_startup:
            self.launch(rpc=rpc)
        else:
            if os.path.exists(self.path_config['startup_path']):
                self.launch(scripts=[self.path_config['startup_path']], rpc=rpc)
            else:
                self.launch(rpc=rpc)


class StoreOptions(argparse.Action):
    """ Subclass of hatsploit module.

    This subclass of hatsploit module is a storage for command-line
    options for payload generator CLI.
    """

    def __call__(self, parser: Any, namespace: Any, values: str,
                 option_string: Optional[str] = None) -> None:
        """ Create a namespace for options.

        :param Any parser: parser
        :param Any namespace: namespace
        :param str value: values splitted by comma
        :param Optional[str] option_string: option string
        :return None: None
        """

        options = {}

        for kv in values.split(","):
            k, v = kv.split("=")
            options[k] = v

        setattr(namespace, self.dest, options)


class HatSploitGen(HatSploit):
    """ Main class of hatsploit module.

    This main class of hatsploit module is a payload generator
    CLI interface.
    """

    def __init__(self) -> None:
        super().__init__()

        self.hatasm = HatAsm()
        self.payloads = Payloads()
        self.encoders = Encoders()

        self.show = Show()

        self.badges = Badges()
        self.tables = Tables()
        self.config = Config()

        self.builder = Builder()
        self.db = DB()

    def cli(self) -> None:
        """ Main command-line arguments handler.

        :return None: None
        """

        if not self.initialize(silent=True):
            return

        description = "Native HatSploit Framework advanced payload generator."
        parser = argparse.ArgumentParser(description=description)
        parser.add_argument(
            '-p',
            '--payload',
            dest='payload',
            help='HatSploit payload.',
        )
        parser.add_argument(
            '-e',
            '--encoder',
            dest='encoder',
            help='HatSploit encoder.',
        )
        parser.add_argument(
            '--platform',
            dest='platform',
            help='Payload platform.',
        )
        parser.add_argument(
            '--arch',
            dest='arch',
            help='Payload architecture',
        )
        parser.add_argument(
            '-f',
            '--format',
            dest='format',
            help='Generate payload with custom format.'
        )
        parser.add_argument(
            '--formats',
            dest='formats',
            action='store_true',
            help='List all formats.',
        )
        parser.add_argument(
            '--payloads',
            dest='payloads',
            action='store_true',
            help='List all payloads.',
        )
        parser.add_argument(
            '--encoders',
            dest='encoders',
            action='store_true',
            help='List all encoders.',
        )
        parser.add_argument(
            '--options',
            dest='options',
            action=StoreOptions,
            help='Add options to encoder/payload.',
            metavar='option1=value1,option2=value2,...'
        )
        parser.add_argument(
            '-i',
            '--iterations',
            dest='iterations',
            type=int,
            help='Number of encoding iterations.'
        )
        parser.add_argument(
            '-b',
            '--badchars',
            dest='badchars',
            help='Bad characters to omit (e.g. \\x00).'
        )
        parser.add_argument(
            '--pack',
            dest='pack',
            action='store_true',
            help='Pack payload as ELF, PE or Mach-O depending on platform. (required --arch and --platform)',
        )
        parser.add_argument(
            '--implant',
            dest='implant',
            action='store_true',
            help='Output implant instead of complete payload.'
        )
        parser.add_argument(
            '-a',
            '--assembly',
            dest='assembly',
            help='Show assembly for payloads. (requires --arch)'
        )
        parser.add_argument(
            '-o',
            '--output',
            dest='output',
            help='Output file to write payload to.'
        )
        parser.add_argument(
            '-c',
            '--custom',
            dest='custom',
            help='Specify custom payloads path.'
        )
        args = parser.parse_args()

        if args.custom:
            self.badges.print_process(f"Using {args.custom} as custom payload path...")

            self.builder.build_payload_database(
                args.custom, self.config.path_config['db_path'] + 'custom.json')
            self.db.connect_payload_database(
                'custom', self.config.path_config['db_path'] + 'custom.json')

        if args.payloads or args.encoders:
            query = ''
            if args.platform:
                query += args.platform

            if args.arch:
                query += '/' + args.arch

            if args.payloads:
                self.show.show_search_payloads(
                    self.payloads.get_payloads(), query)
            elif args.encoders:
                self.show.show_search_encoders(
                    self.encoders.get_encoders(), query)

        elif args.formats:
            if not args.platform:
                data = []

                for format in EXEC_FORMATS:
                    platforms = ', '.join([str(p) for p in EXEC_FORMATS[format]])
                    data.append((format, platforms))

                self.tables.print_table("Formats", ('Format', 'Platforms'), *data)

            else:
                formats = []

                for format in EXEC_FORMATS:
                    if args.platform in EXEC_FORMATS[format]:
                        formats.append(format)

                data = [(args.platform, ', '.join(formats))]
                self.tables.print_table("Formats", ('Platform', 'Formats'), *data)

        elif args.payload:
            self.badges.print_process(f"Attempting to generate {args.payload}...")

            options = {}

            if args.options:
                options = args.options

            if args.encoder and args.iterations:
                self.badges.print_information(f"Using {str(args.iterations)} as a number of times to encode.")
                options['iterations'] = args.iterations

            if args.badchars:
                self.badges.print_information(f"Trying to avoid these bad characters: {args.badchars}")
                options['badchars'] = args.badchars

            if args.encoder:
                self.badges.print_information(f"Payload will be encoded with {args.encoder}")

            payload = self.payloads.get_payload(args.payload)
            if not payload:
                self.badges.print_error(f"Invalid payload: {args.payload}!")
                return

            details = payload.details
            payload = self.payloads.generate_payload(
                args.payload, options, args.encoder, 'implant' if args.implant else 'run')

            if args.pack:
                payload = self.payloads.pack_payload(
                    payload, details['Platform'], details['Arch'], args.format)

            if not payload:
                self.badges.print_error(f"Invalid format: {args.format}!")
                return

            if not args.output:
                self.badges.print_process("Writing raw payload...")

                if isinstance(payload, bytes):
                    if args.assembly:
                        hexdump = self.hatasm.hexdump_asm(str(details['Arch']), code=payload)
                    else:
                        hexdump = self.hatasm.hexdump(payload)

                    for line in hexdump:
                        self.badges.print_empty(line)
                else:
                    self.badges.print_empty(payload)

            else:
                with open(args.output, 'wb') as f:
                    self.badges.print_process(f"Saving payload to {args.output}...")
                    f.write(payload)

        else:
            parser.print_help()
