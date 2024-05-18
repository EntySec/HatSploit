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

import os
import sys

from badges import Badges

from hatsploit.core.db.importer import Importer
from hatsploit.lib.config import Config


class Check(object):
    """ Subclass of hatsploit.core.utils module.

    This subclass of hatsploit.core.utils module is intended for
    providing tools for checking HatSploit modules, payloads, plugins and
    encoders.
    """

    def __init__(self) -> None:
        super().__init__()

        self.config = Config()
        self.importer = Importer()
        self.badges = Badges()

    def check_modules(self) -> bool:
        """ Check base modules.

        :return bool: True if success else False
        """

        one_fail = False
        self.badges.print_process("Checking all base modules...")

        modules_path = os.path.normpath(self.config.path_config['modules_path'])

        for dir, _, files in os.walk(modules_path):
            for file in files:
                if file.endswith('.py') and file != '__init__.py':
                    module = dir + '/' + file[:-3]

                    try:
                        module_object = self.importer.import_module(module)
                        keys = [
                            'Category',
                            'Name',
                            'Module',
                            'Authors',
                            'Description',
                            'Platform',
                            'Rank',
                        ]

                        assert all(key in module_object.details for key in keys)
                        self.badges.print_success(f"{module}: OK")

                    except Exception as e:
                        self.badges.print_error(str(e))
                        self.badges.print_error(f"{module}: FAIL")

                        one_fail = True

        return not one_fail

    def check_encoders(self) -> None:
        """ Check base encoders.

        :return bool: True if success else False
        """

        one_fail = False
        self.badges.print_process("Checking all base encoders...")

        encoders_path = os.path.normpath(self.config.path_config['encoders_path'])

        for dir, _, files in os.walk(encoders_path):
            for file in files:
                if file.endswith('.py') and file != '__init__.py':
                    encoder = dir + '/' + file[:-3]

                    try:
                        encoder_object = self.importer.import_encoder(encoder)
                        keys = [
                            'Name',
                            'Encoder',
                            'Authors',
                            'Description',
                            'Arch',
                        ]

                        assert all(key in encoder_object.details for key in keys)
                        self.badges.print_success(f"{encoder}: OK")

                    except Exception as e:
                        self.badges.print_error(str(e))
                        self.badges.print_error(f"{encoder}: FAIL")

                        one_fail = True

        return not one_fail

    def check_payloads(self) -> bool:
        """ Check base payloads.

        :return bool: True if success else False
        """

        one_fail = False
        self.badges.print_process("Checking all base payloads...")

        payloads_path = os.path.normpath(self.config.path_config['payloads_path'])

        for dir, _, files in os.walk(payloads_path):
            for file in files:
                if file.endswith('.py') and file != '__init__.py':
                    payload = dir + '/' + file[:-3]

                    try:
                        payload_object = self.importer.import_payload(payload)
                        keys = [
                            'Name',
                            'Payload',
                            'Authors',
                            'Description',
                            'Arch',
                            'Platform',
                            'Rank',
                            'Type',
                        ]

                        assert all(key in payload_object.details for key in keys)
                        self.badges.print_success(f"{payload}: OK")

                    except Exception as e:
                        self.badges.print_error(str(e))
                        self.badges.print_error(f"{payload}: FAIL")

                        one_fail = True

        return not one_fail

    def check_plugins(self) -> bool:
        """ Check base plugins.

        :return bool: True if success else False
        """

        one_fail = False
        self.badges.print_process("Checking all base plugins...")

        plugins_path = os.path.normpath(self.config.path_config['plugins_path'])

        for dir, _, files in os.walk(plugins_path):
            for file in files:
                if file.endswith('.py') and file != '__init__.py':
                    plugin = dir + '/' + file[:-3]

                    try:
                        plugin_object = self.importer.import_plugin(plugin)
                        keys = ['Name', 'Authors', 'Description']

                        assert all(key in plugin_object.details for key in keys)
                        self.badges.print_success(f"{plugin}: OK")

                    except Exception as e:
                        self.badges.print_error(str(e))
                        self.badges.print_error(f"{plugin}: FAIL")

                        one_fail = True

        return not one_fail

    def check_all(self) -> bool:
        """ Check base modules, encoders, payloads and plugins

        :return bool: True if success else False
        """

        fails = list()

        fails.append(self.check_modules())
        fails.append(self.check_payloads())
        fails.append(self.check_encoders())
        fails.append(self.check_plugins())

        for fail in fails:
            if not fail:
                self.badges.print_error("Not all checks passed!")
                return False

        self.badges.print_success("All checks passed!")
        return True
