"""
MIT License

Copyright (c) 2020-2022 EntySec

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

import copy
import os
from pex.type import Type

from hatsploit.core.cli.badges import Badges
from hatsploit.core.db.importer import Importer
from hatsploit.lib.encoders import Encoders
from hatsploit.lib.options import Options
from hatsploit.lib.payloads import Payloads
from hatsploit.lib.sessions import Sessions
from hatsploit.lib.storage import LocalStorage


class Modules(object):
    def __init__(self):
        super().__init__()

        self.types = Type()

        self.badges = Badges()
        self.importer = Importer()

        self.options = Options()
        self.payloads = Payloads()
        self.encoders = Encoders()
        self.sessions = Sessions()
        self.local_storage = LocalStorage()

    def modules_completer(self, text):
        modules = self.get_modules()
        matches = []

        if modules:
            for database in modules:
                for module in modules[database]:
                    if module.startswith(text):
                        matches.append(module)

        return matches

    def get_modules(self):
        return self.local_storage.get("modules")

    def get_imported_modules(self):
        return self.local_storage.get("imported_modules")

    def get_database(self, name):
        all_modules = self.get_modules()
        if all_modules:
            for database in all_modules:
                modules = all_modules[database]

                if name in modules:
                    return database
        return None

    def get_module(self, module):
        module_object = self.get_module_object(module)
        try:
            imported_module = self.importer.import_module(module_object['Path'])
        except Exception:
            return None
        return imported_module

    def get_module_object(self, module):
        if self.check_exist(module):
            database = self.get_database(module)
            return self.get_modules()[database][module]
        return None

    def get_current_module(self):
        if self.local_storage.get("current_module"):
            return self.local_storage.get_array(
                "current_module",
                self.local_storage.get("current_module_number")
            )
        return None

    def get_number_module(self, number):
        modules_shorts = self.local_storage.get("module_shorts")

        if modules_shorts:
            if number in modules_shorts:
                return modules_shorts[number]
        return None

    def search_module(self, name):
        modules = self.get_modules()

        for database in modules:
            for module in modules[database]:
                if modules[database][module]['Name'].lower() == name.lower():
                    return modules[database][module]['Module']
        return None

    def import_module(self, module):
        module_object = self.get_module(module)

        if module_object:
            if not self.get_imported_modules():
                self.local_storage.set("imported_modules", {})
            self.local_storage.update("imported_modules", {module: module_object})
        return module_object

    def check_exist(self, module):
        all_modules = self.get_modules()
        if all_modules:
            for database in all_modules:
                modules = all_modules[database]

                if module in modules:
                    return True
        return False

    def check_imported(self, module):
        imported_modules = self.get_imported_modules()
        if imported_modules:
            if module in imported_modules:
                return True
        return False

    def check_if_already_used(self, module):
        current_module = self.get_current_module()

        if current_module:
            if module == current_module.details['Module']:
                return True
        return False

    def use_module(self, module):
        if module.isdigit():
            number = int(module)
            module = self.get_number_module(number)

            if not module:
                raise RuntimeError(f"Invalid module number: {str(number)}!")

        if not self.check_if_already_used(module):
            if self.check_exist(module):
                self.add_module(module)
            else:
                raise RuntimeError(f"Invalid module: {module}!")

    def add_module(self, module):
        imported_modules = self.get_imported_modules()

        if self.check_imported(module):
            module_object = imported_modules[module]
            self.add_to_global(module_object)
        else:
            module_object = self.import_module(module)
            if module_object:
                if hasattr(module_object, "payload"):
                    payload_name = module_object.payload['Value']

                    if payload_name:
                        self.badges.print_process(f"Using default payload {payload_name}...")

                        if self.payloads.check_exist(payload_name):
                            self.payloads.add_payload(module, payload_name)
                            self.add_to_global(module_object)

                            current_payload = self.payloads.get_current_payload(module_object)
                            self.options.add_handler_options(module_object, current_payload)

                            return

                        raise RuntimeError(f"Invalid default payload: {payload_name}!")

                self.add_to_global(module_object)

                current_payload = self.payloads.get_current_payload(module_object)
                self.options.add_handler_options(module_object, current_payload)
            else:
                raise RuntimeError(f"Failed to select module from database: {module}!")

    def add_to_global(self, module_object):
        if self.get_current_module():
            self.local_storage.add_array("current_module", '')
            self.local_storage.set("current_module_number", self.local_storage.get("current_module_number") + 1)
            self.local_storage.set_array("current_module", self.local_storage.get("current_module_number"),
                                         module_object)
        else:
            self.local_storage.set("current_module", [])
            self.local_storage.set("current_module_number", 0)
            self.local_storage.add_array("current_module", '')
            self.local_storage.set_array("current_module", self.local_storage.get("current_module_number"),
                                         module_object)

    def go_back(self):
        if self.get_current_module():
            self.local_storage.set("current_module_number", self.local_storage.get("current_module_number") - 1)
            self.local_storage.set("current_module", self.local_storage.get("current_module")[0:-1])
            if not self.local_storage.get("current_module"):
                self.local_storage.set("current_module_number", 0)

    @staticmethod
    def run_module(current_module):
        if hasattr(current_module, "check"):
            if current_module.check():
                current_module.run()
        else:
            current_module.run()

    def entry_to_module(self, current_module):
        values = []

        for option in current_module.options:
            opt = current_module.options[option]
            val = str(opt['Value'])

            if val.startswith('file:') and len(val) > 5:
                file = val[5:]

                with open(file, 'r') as f:
                    vals = f.read().strip()
                    values.append(vals.split('\n'))

        if not values:
            self.run_module(current_module)
            return

        if not all(len(value) == len(values[0]) for value in values):
            raise RuntimeError("All files should contain equal number of values!")

        save = copy.deepcopy(current_module.options)
        for i in range(0, len(values[0])):
            count = 0

            for option in current_module.options:
                opt = current_module.options[option]
                val = str(opt['Value'])

                if val.startswith('file:') and len(val) > 5:
                    current_module.options[option]['Value'] = values[count][i]
                    count += 1

            try:
                self.run_module(current_module)
            except (KeyboardInterrupt, EOFError):
                pass

            current_module.options = save
            save = copy.deepcopy(current_module.options)

    @staticmethod
    def compare_type(name, value, checker):
        value = str(value)

        if value.startswith('file:') and len(value) > 5:
            file = value.split(':')[1]

            if not os.path.isfile(file):
                raise RuntimeError(f"Local file: {file}: does not exist!")

            with open(file, 'r') as f:
                for line in f.read().split('\n'):
                    if line.strip():
                        if not checker(line.strip()):
                            raise RuntimeError(f"File contains invalid value, expected valid {name}!")
            return

        if not checker(value):
            raise RuntimeError(f"Invalid value, expected valid {name}!")

    def compare_session(self, value_type, value):
        current_module = self.get_current_module()

        if current_module:
            session_platforms = value_type['session']['Platforms']
            session_platform = current_module.details['Platform']
            session_type = value_type['session']['Type']

            if not session_platforms:
                if not self.sessions.check_exist(value, session_platform, session_type):
                    raise RuntimeError("Invalid value, expected valid session!")
            else:
                session = 0
                for platform in session_platforms:
                    if self.sessions.check_exist(value, platform.strip(), session_type):
                        session = 1
                        break

                if not session:
                    raise RuntimeError("Invalid value, expected valid session!")
        else:
            raise RuntimeError("Invalid value, expected valid session!")

    def compare_types(self, value_type, value):
        if value_type and not isinstance(value_type, dict):
            if value_type.lower() in self.types.types:
                return self.compare_type(value_type.lower(), value, self.types.types[value_type.lower()])

            if value_type.lower() == 'payload':
                current_module = self.get_current_module()

                if current_module:
                    module_name = current_module.details['Module']
                    module_payload = current_module.payload

                    types = module_payload['Types']
                    platforms = module_payload['Platforms']
                    architectures = module_payload['Architectures']

                    if self.payloads.check_module_compatible(value, types, platforms, architectures):
                        self.payloads.add_payload(module_name, value)
                        return

                raise RuntimeError("Invalid value, expected valid payload!")

            if value_type.lower() == 'encoder':
                current_module = self.get_current_module()
                current_payload = self.payloads.get_current_payload(current_module)

                if current_module and current_payload:
                    architecture = current_payload.details['Architecture']

                    if self.encoders.check_payload_compatible(value, architecture):
                        self.encoders.add_encoder(
                            current_module.details['Module'],
                            current_payload.details['Payload'], value)
                        return

                raise RuntimeError("Invalid value, expected valid encoder!")

        if isinstance(value_type, dict):
            if 'session' in value_type:
                value = str(value)

                if value.startswith('file:') and len(value) > 5 and module:
                    file = value.split(':')[1]

                    if not os.path.isfile(file):
                        raise RuntimeError(f"Local file: {file}: does not exist!")

                    with open(file, 'r') as f:
                        for line in f.read().split('\n'):
                            if line.strip():
                                if not self.compare_session(value_type, line.strip()):
                                    raise RuntimeError(f"File contains invalid value, expected valid session!")
                    return

                return self.compare_session(value_type, value)

    def find_shorts(self, value_type, value):
        if value_type == 'payload':
            payloads_shorts = self.local_storage.get("payload_shorts")

            if payloads_shorts:
                if value.isdigit():
                    payload_number = int(value)

                    if payload_number in payloads_shorts:
                        value = payloads_shorts[payload_number]

        elif value_type == 'encoder':
            encoders_shorts = self.local_storage.get("encoder_shorts")

            if encoders_shorts:
                if value.isdigit():
                    encoder_number = int(value)

                    if encoder_number in encoders_shorts:
                        value = encoders_shorts[encoder_number]

        return value

    def set_option_value(self, current, options, option, value):
        if option in options:
            value_type = options[option]['Type']
            value = self.find_shorts(value_type, value)

            if value:
                self.compare_types(value_type, value)

            options[option]['Value'] = value

            if hasattr(current, "payload"):
                if option.lower() == 'blinder' and value.lower() in ['y', 'yes']:
                    current.payload['Value'] = None

                if option.lower() == 'payload':
                    current.payload['Value'] = value

            self.badges.print_information(option + " ==> " + value)

            return True
        return False

    def set_current_module_option(self, option, value):
        current_module = self.get_current_module()
        current_payload = self.payloads.get_current_payload(current_module)

        if current_module:
            if not hasattr(current_module, "options") and not hasattr(current_module, "advanced"):
                if not hasattr(current_module, "payload"):
                    raise RuntimeWarning("Module has no options.")

            if hasattr(current_module, "options"):
                if self.set_option_value(current_module, current_module.options, option, value):
                    current_payload = self.payloads.get_current_payload(current_module)
                    return self.options.add_handler_options(current_module, current_payload)

            if hasattr(current_module, "advanced"):
                if self.set_option_value(current_module, current_module.advanced, option, value):
                    return self.options.add_handler_options(current_module, current_payload)

            if hasattr(current_module, "payload"):
                if current_payload:
                    current_encoder = self.encoders.get_current_encoder(current_module, current_payload)

                    if hasattr(current_payload, "options"):
                        if self.set_option_value(current_payload, current_payload.options, option, value):
                            return self.options.add_handler_options(current_module, current_payload)

                    if hasattr(current_payload, "advanced"):
                        if self.set_option_value(current_payload, current_payload.advanced, option, value):
                            return self.options.add_handler_options(current_module, current_payload)

                    if current_encoder:
                        if hasattr(current_encoder, "options"):
                            if self.set_option_value(current_encoder, current_encoder.options, option, value):
                                return self.options.add_handler_options(current_module, current_payload)

                        if hasattr(current_encoder, "advanced"):
                            if self.set_option_value(current_encoder, current_encoder.advanced, option, value):
                                return self.options.add_handler_options(current_module, current_payload)

            raise RuntimeError("Unrecognized module option!")
        raise RuntimeWarning("No module selected.")

    @staticmethod
    def validate_options(module_object):
        current_module = module_object
        missed = ""

        if hasattr(current_module, "options"):
            for option in current_module.options:
                current_option = current_module.options[option]
                if not current_option['Value'] and current_option['Value'] != 0 and current_option['Required']:
                    missed += option + ', '

        return missed

    def check_current_module(self):
        current_module = self.get_current_module()

        if current_module:
            if hasattr(current_module, "check"):
                return current_module.check()

        return False

    def run_current_module(self, loop=False):
        if not loop:
            if exception_handler is not None:
                return exception_handler(
                    self.prepare_and_entry
                )
            else:
                return self.prepare_and_entry()

        while True:
            if exception_handler is not None:
                exception_handler(
                    self.prepare_and_entry
                )
            else:
                self.prepare_and_entry()

    def prepare_and_entry(self):
        current_module = copy.deepcopy(self.get_current_module())

        if current_module:
            current_module_name = current_module.details['Module']

            current_payload = copy.deepcopy(
                self.payloads.get_current_payload(current_module))

            missed = self.validate_options(current_module)
            if current_payload:
                missed += self.payloads.validate_options(current_payload)

            if missed:
                raise RuntimeError(
                    f"These options are failed to validate: {missed[:-2]}!")

            try:
                self.badges.print_empty()

                if current_payload:
                    current_encoder = self.encoders.get_current_encoder(
                        current_module, current_payload)
                    payload = self.payloads.run_payload(
                        current_payload, current_encoder)

                    current_module.payload['Payload'] = payload
                    current_module.payload['Object'] = current_payload

                    current_module.payload['Executable'] = self.payloads.pack_payload(
                        current_module.payload['Payload'],
                        current_payload.details['Platform'],
                        current_payload.details['Architecture']
                    )

                self.entry_to_module(current_module)

                self.badges.print_success(
                    f"{current_module_name.split('/')[0].title()} module completed!")
            except (KeyboardInterrupt, EOFError):
                raise RuntimeWarning(
                    f"{current_module_name.split('/')[0].title()} module interrupted.")

            if current_payload:
                del current_module.payload['Payload']
                del current_module.payload['Executable']
        else:
            raise RuntimeWarning("No module selected.")
