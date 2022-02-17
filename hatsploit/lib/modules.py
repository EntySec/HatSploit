#!/usr/bin/env python3

#
# MIT License
#
# Copyright (c) 2020-2022 EntySec
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

import os
import copy

from hatsploit.core.base.types import Types
from hatsploit.core.cli.badges import Badges
from hatsploit.core.db.importer import Importer
from hatsploit.lib.payloads import Payloads
from hatsploit.lib.sessions import Sessions
from hatsploit.lib.storage import LocalStorage


class Modules:
    types = Types()
    badges = Badges()
    sessions = Sessions()
    payloads = Payloads()
    local_storage = LocalStorage()
    importer = Importer()

    def get_modules(self):
        return self.local_storage.get("modules")

    def get_imported_modules(self):
        return self.local_storage.get("imported_modules")

    def modules_completer(self, text):
        modules = self.get_modules()
        matches = []

        for database in modules:
            for module in modules[database]:
                if module.endswith(text):
                    matches.append(module)

        return matches

    def check_exist(self, name):
        all_modules = self.get_modules()
        if all_modules:
            for database in all_modules:
                modules = all_modules[database]

                if name in modules:
                    return True
        return False

    def check_imported(self, name):
        imported_modules = self.get_imported_modules()
        if imported_modules:
            if name in imported_modules:
                return True
        return False

    def check_current_module(self):
        if self.local_storage.get("current_module"):
            if len(self.local_storage.get("current_module")) > 0:
                return True
        return False

    def check_if_already_used(self, module):
        if self.check_current_module():
            if module == self.get_current_module_name():
                return True
        return False

    def get_module_object(self, name):
        if self.check_exist(name):
            database = self.get_database(name)
            return self.get_modules()[database][name]
        return None

    def get_current_module_object(self):
        if self.check_current_module():
            return self.local_storage.get_array("current_module", self.local_storage.get("current_module_number"))
        return None

    def get_current_module_platform(self):
        if self.check_current_module():
            return self.local_storage.get_array("current_module",
                                                self.local_storage.get("current_module_number")).details['Platform']
        return None

    def get_current_module_name(self):
        if self.check_current_module():
            return self.local_storage.get_array("current_module",
                                                self.local_storage.get("current_module_number")).details['Module']
        return None

    def get_database(self, name):
        all_modules = self.get_modules()
        if all_modules:
            for database in all_modules:
                modules = all_modules[database]

                if name in modules:
                    return database
        return None

    def compare_type(self, name, value, checker, module=True):
        value = str(value)

        if value.startswith('file:') and len(value) > 5 and module:
            file = value.split(':')[1]

            if not os.path.isfile(file):
                self.badges.print_error(f"Local file: {file}: does not exist!")
                return False

            with open(file, 'r') as f:
                for line in f.read().split('\n'):
                    if line.strip():
                        if not checker(line.strip()):
                            self.badges.print_error(f"File contains invalid value, expected valid {name}!")
                            return False
            return True

        if not checker(value):
            self.badges.print_error(f"Invalid value, expected valid {name}!")
            return False

        return True

    def compare_session(self, value_type, value):
        session = value_type.lower().replace(' ', '')
        session = session.split('->')

        session_platforms = []
        session_platform = self.get_current_module_platform()
        session_type = "shell"

        if len(session) == 2:
            if session[1].startswith('[') and session[1].endswith(']'):
                session_platforms = session[1][1:-1].split(',')
            else:
                session_type = session[1]

        elif len(session) == 3:
            if session[1].startswith('[') and session[1].endswith(']'):
                session_platforms = session[1][1:-1].split(',')
            else:
                session_type = session[1]

            if session[2].startswith('[') and session[2].endswith(']'):
                session_platforms = session[2][1:-1].split(',')
            else:
                session_type = session[2]

        if not session_platforms:
            if not self.sessions.check_exist(value, session_platform, session_type):
                self.badges.print_error("Invalid value, expected valid session!")
                return False
        else:
            session = 0
            for platform in session_platforms:
                if self.sessions.check_exist(value, platform.strip(), session_type):
                    session = 1
                    break

            if not session:
                self.badges.print_error("Invalid value, expected valid session!")
                return False

        return True

    def compare_types(self, value_type, value, module=True):
        if value_type and not value_type.lower == 'all':
            if value_type.lower() == 'mac':
                return self.compare_type("MAC", value, self.types.is_mac, module)

            if value_type.lower() == 'ip':
                return self.compare_type("IP", value, self.types.is_ip, module)

            if value_type.lower() == 'ipv4':
                return self.compare_type("IPv4", value, self.types.is_ipv4, module)

            if value_type.lower() == 'ipv6':
                return self.compare_type("IPv6", value, self.types.is_ipv6, module)

            if value_type.lower() == 'ipv4_range':
                return self.compare_type("IPv4 range", value, self.types.is_ipv4_range, module)

            if value_type.lower() == 'ipv6_range':
                return self.compare_type("IPv6 range", value, self.types.is_ipv6_range, module)

            if value_type.lower() == 'port':
                return self.compare_type("port", value, self.types.is_port, module)

            if value_type.lower() == 'port_range':
                return self.compare_type("port range", value, self.types.is_port_range, module)

            if value_type.lower() == 'number':
                return self.compare_type("number", value, self.types.is_number, module)

            if value_type.lower() == 'integer':
                return self.compare_type("integer", value, self.types.is_integer, module)

            if value_type.lower() == 'float':
                return self.compare_type("float", value, self.types.is_float, module)

            if value_type.lower() == 'boolean':
                return self.compare_type("boolean", value, self.types.is_boolean, module)

            if value_type.lower() == 'payload':
                current_module = self.get_current_module_object()
                module_name = self.get_current_module_name()
                module_payload = current_module.payload

                categories = module_payload['Categories']
                types = module_payload['Types']
                platforms = module_payload['Platforms']
                architectures = module_payload['Architectures']

                if self.payloads.check_module_compatible(value, categories, types, platforms, architectures):
                    if self.payloads.add_payload(module_name, value):
                        return True

                self.badges.print_error("Invalid valud, expected valid payload!")
                return False

            if 'session' in value_type.lower():
                value = str(value)

                if value.startswith('file:') and len(value) > 5 and module:
                    file = value.split(':')[1]

                    if not os.path.isfile(file):
                        self.badges.print_error(f"Local file: {file}: does not exist!")
                        return False

                    with open(file, 'r') as f:
                        for line in f.read().split('\n'):
                            if line.strip():
                                if not self.compare_session(value_type, line.strip()):
                                    self.badges.print_error(f"File contains invalid value, expected valid session!")
                                    return False
                    return True

                return self.compare_session(value_type, value)

        return True

    def set_current_module_option(self, option, value):
        if self.check_current_module():
            current_module = self.get_current_module_object()

            if not hasattr(current_module, "options") and not hasattr(current_module, "payload"):
                self.badges.print_warning("Module has no options.")
                return

            if hasattr(current_module, "options"):
                if option in current_module.options:
                    value_type = current_module.options[option]['Type']

                    if value_type == 'payload':
                        payloads_shorts = self.local_storage.get("payload_shorts")

                        if payloads_shorts:
                            if value.isdigit():
                                payload_number = int(value)

                                if payload_number in payloads_shorts:
                                    value = payloads_shorts[payload_number]

                    if self.compare_types(value_type, value):
                        self.badges.print_information(option + " ==> " + value)

                        if option.lower() == 'blinder':
                            if value.lower() in ['y', 'yes']:
                                current_module.payload['Value'] = None

                        if value_type == 'payload':
                            self.local_storage.set_module_payload(
                                "current_module",
                                self.local_storage.get("current_module_number"),
                                value
                            )
                        else:
                            self.local_storage.set_module_option(
                                "current_module",
                                self.local_storage.get("current_module_number"),
                                option,
                                value
                            )
                    return

            if hasattr(current_module, "payload"):
                current_payload = self.payloads.get_current_payload()
                if current_payload and hasattr(current_payload, "options"):
                    if option in current_payload.options:
                        value_type = current_payload.options[option]['Type']

                        if self.compare_types(value_type, value, False):
                            self.badges.print_information(option + " ==> " + value)
                            self.local_storage.set_payload_option(current_module.details['Module'],
                                                                  current_payload.details['Payload'], option, value)
                    else:
                        self.badges.print_error("Unrecognized option!")
                else:
                    self.badges.print_error("Unrecognized option!")
            else:
                self.badges.print_error("Unrecognized option!")
        else:
            self.badges.print_warning("No module selected.")

    def import_module(self, name):
        modules = self.get_module_object(name)
        try:
            module_object = self.importer.import_module(modules['Path'])
            if not self.get_imported_modules():
                self.local_storage.set("imported_modules", {})
            self.local_storage.update("imported_modules", {name: module_object})
        except Exception:
            return None
        return module_object

    def add_module(self, name):
        imported_modules = self.get_imported_modules()

        if self.check_imported(name):
            module_object = imported_modules[name]
            self.add_to_global(module_object)
        else:
            module_object = self.import_module(name)
            if module_object:
                if hasattr(module_object, "payload"):
                    payload_name = module_object.payload['Value']

                    if payload_name:
                        self.badges.print_process(f"Using default payload {payload_name}...")

                        if self.payloads.check_exist(payload_name):
                            if self.payloads.add_payload(name, payload_name):
                                self.add_to_global(module_object)
                            return

                        self.badges.print_error("Invalid default payload!")
                        return

                self.add_to_global(module_object)
            else:
                self.badges.print_error("Failed to select module from database!")

    def add_to_global(self, module_object):
        if self.check_current_module():
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

    def use_module(self, module):
        modules_shorts = self.local_storage.get("module_shorts")

        if modules_shorts:
            if module.isdigit():
                module_number = int(module)

                if module_number in modules_shorts:
                    module = modules_shorts[module_number]

        if not self.check_if_already_used(module):
            if self.check_exist(module):
                self.add_module(module)
            else:
                self.badges.print_error("Invalid module!")

    def go_back(self):
        if self.check_current_module():
            self.local_storage.set("current_module_number", self.local_storage.get("current_module_number") - 1)
            self.local_storage.set("current_module", self.local_storage.get("current_module")[0:-1])
            if not self.local_storage.get("current_module"):
                self.local_storage.set("current_module_number", 0)

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
            current_module.run()
            return

        if not all(len(value) == len(values[0]) for value in values):
            self.badges.print_error("All files should contain equal number of values!")
            return

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
                current_module.run()
            except (KeyboardInterrupt, EOFError):
                pass

            current_module.options = save
            save = copy.deepcopy(current_module.options)

    def validate_options(self, module_object):
        current_module = module_object
        missed = ""

        if hasattr(current_module, "options"):
            for option in current_module.options:
                current_option = current_module.options[option]
                if not current_option['Value'] and current_option['Value'] != 0 and current_option['Required']:
                    missed += option + ', '

        return missed

    def run_current_module(self):
        if self.check_current_module():
            current_module = self.get_current_module_object()
            current_module_name = self.get_current_module_name()

            current_payload = self.payloads.get_current_payload()
            payload_data = {}

            missed = self.validate_options(current_module)
            if current_payload:
                missed += self.payloads.validate_options(current_payload)

            if missed:
                self.badges.print_error(f"These options are failed to validate: {missed[:-2]}!")
            else:
                try:
                    if current_payload:
                        payload_data = self.payloads.run_payload(current_payload)
                        for entry in payload_data:
                            current_module.payload[entry] = payload_data[entry]

                    self.badges.print_empty()
                    self.entry_to_module(current_module)

                    self.badges.print_success(f"{current_module_name.split('/')[0].title()} module completed!")
                except (KeyboardInterrupt, EOFError):
                    self.badges.print_warning(f"{current_module_name.split('/')[0].title()} module interrupted.")

                except Exception as e:
                    self.badges.print_error(f"An error occurred in module: {str(e)}!")
                    self.badges.print_error(f"{current_module_name.split('/')[0].title()} module failed!")

                if current_payload:
                    for entry in payload_data:
                        del current_module.payload[entry]
        else:
            self.badges.print_warning("No module selected.")
