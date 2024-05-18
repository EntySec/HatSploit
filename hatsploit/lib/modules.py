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

import copy
import os

from typing import Union, Optional, Callable

from badges import Badges

from hatsploit.core.db.importer import Importer

from hatsploit.lib.encoder import Encoder
from hatsploit.lib.encoders import Encoders
from hatsploit.lib.options import Options
from hatsploit.lib.payload import Payload
from hatsploit.lib.payloads import Payloads
from hatsploit.lib.sessions import Sessions
from hatsploit.lib.storage import LocalStorage
from hatsploit.lib.module import Module


class Modules(object):
    """ Subclass of hatsploit.lib module.

    This subclass of hatsploit.lib module is intended for providing
    tools for working with HatSploit modules.
    """

    def __init__(self) -> None:
        super().__init__()

        self.badges = Badges()
        self.importer = Importer()

        self.options = Options()
        self.payloads = Payloads()
        self.encoders = Encoders()
        self.sessions = Sessions()
        self.local_storage = LocalStorage()

    def modules_completer(self, text: str) -> list:
        """ Tab-completion for modules.

        :param str text: text to complete
        :return list: list of completions
        """

        modules = self.get_modules()
        matches = []

        if modules:
            for database in modules:
                for module in modules[database]:
                    if module.startswith(text):
                        matches.append(module)

        return matches

    def get_modules(self) -> dict:
        """ Get all modules from local storage.

        :return dict: modules, module names as keys and
        module objects as items
        """

        return self.local_storage.get("modules", {})

    def get_imported_modules(self) -> dict:
        """ Get all imported modules from local storage.

        :return dict: modules, module name as keys and
        module objects as items
        """

        return self.local_storage.get("imported_modules", {})

    def get_database(self, module: str) -> str:
        """ Get database in which specific module exists.

        :param str module: module name
        :return str: database name
        """

        all_modules = self.get_modules()

        if all_modules:
            for database in all_modules:
                modules = all_modules[database]

                if module in modules:
                    return database

        return ''

    def get_module(self, module: str) -> Union[Module, None]:
        """ Import and get imported module.

        :param str module: module name
        :return Union[Module, None]: imported module, None if failed to import
        """

        module_object = self.get_module_object(module)

        try:
            imported_module = self.importer.import_module(module_object['Path'])
            self.options.add_options(imported_module)
        except Exception:
            return None

        return imported_module

    def get_module_object(self, module: str) -> dict:
        """ Get module object, this object represents module details
        from the database.

        :param str module: module name
        :return dict: module object, module details
        """

        if self.check_exist(module):
            database = self.get_database(module)

            return self.get_modules()[database][module]
        return {}

    def get_current_module(self) -> Union[Module, None]:
        """ Get current module, this is module which is currently used.

        :return Union[Module, None]: current module, None if no current module
        """

        if self.local_storage.get("current_module"):
            return self.local_storage.get("current_module")[-1]

    def get_number_module(self, number: int) -> str:
        """ Get module name by its number.

        :param int number: module number
        :return str: module name
        """

        module = ''
        module_shorts = self.local_storage.get("module_shorts")

        if module_shorts:
            if number in module_shorts:
                module = module_shorts[number]

        return module

    def search_module(self, name: str) -> str:
        """ Get module name by full module name.

        Note: Module name looks like this:
              - exploit/generic/handler_reverse_tcp
              Full module name looks like this:
              - Reverse TCP Handler

        :param str name: module name
        :return str: module short name
        """

        modules = self.get_modules()

        for database in modules:
            for module in modules[database]:
                if modules[database][module]['Name'].lower() == name.lower():
                    return modules[database][module]['Module']

        return ''

    def import_module(self, module: str) -> Union[Module, None]:
        """ Import module.

        :param str module: module name
        :return Union[Module, None]: imported module, None if failed to import
        """

        module_object = self.get_module(module)

        if module_object:
            if self.get_imported_modules():
                self.local_storage.update("imported_modules", {module: module_object})
            else:
                self.local_storage.set("imported_modules", {module: module_object})

        return module_object

    def check_exist(self, module: str) -> bool:
        """ Check if module exists in the database.

        :param str module: module name
        :return bool: True if exists else False
        """

        all_modules = self.get_modules()

        if all_modules:
            for database in all_modules:
                modules = all_modules[database]

                if module in modules:
                    return True

        return False

    def check_imported(self, module: str) -> bool:
        """ Check if encoder is imported.

        :param str module: module name
        :return bool: True if imported else False
        """

        imported_modules = self.get_imported_modules()

        if imported_modules:
            if module in imported_modules:
                return True

        return False

    def check_if_already_used(self, module: str) -> bool:
        """ Check if module was previously used.

        :param str module: module name
        :return bool: True if was used else False
        """

        current_module = self.get_current_module()

        if current_module:
            if module == current_module.details['Module']:
                return True

        return False

    def use_module(self, module: str) -> None:
        """ Use specific module.

        :param str module: module name or number
        :return None: None
        :raises RuntimeError: with trailing error message
        """

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

    def add_module(self, module: str) -> None:
        """ Add module to the local storage.

        :param str module: module name
        :return None: None
        :raises RuntimeError: with trailing error message
        """

        imported_modules = self.get_imported_modules()

        if self.check_imported(module):
            module_object = imported_modules[module]
            self.add_to_global(module_object)

        else:
            module_object = self.import_module(module)

            if module_object:
                self.add_to_global(module_object)

                if 'Payload' in module_object.details:
                    payload_name = module_object.details['Payload'].get('Value', None)

                    if payload_name:
                        self.badges.print_process(f"Using default payload {payload_name}...")

                        if module_object.set('payload', payload_name):
                            return

                        self.go_back()
                        raise RuntimeError(f"Invalid default payload: {payload_name}!")
            else:
                raise RuntimeError(f"Failed to select module from database: {module}!")

    def add_to_global(self, module: Module) -> None:
        """ Allocate space in local storage for module object.

        :param Module module: module object
        :return None: None
        """

        if self.get_current_module():
            current_module = self.local_storage.get("current_module")
            current_module.append(module)

            self.local_storage.set("current_module", current_module)
        else:
            self.local_storage.set("current_module", [module])

    def go_back(self) -> None:
        """ Go back to the previous module in the local storage.

        :return None: None
        """

        if self.get_current_module():
            current_module = self.local_storage.get("current_module")
            current_module.pop()

            self.local_storage.set("current_module", current_module)

    @staticmethod
    def run_module(module: Module) -> None:
        """ Run module.

        :param Module module: module object
        :raises RuntimeError: with trailing error message
        :return None: None
        """

        if not hasattr(module, "check"):
            module.run()
            return

        if not module.check():
            raise RuntimeWarning(
                f"{module.details['Category'].title()} module failed! (not vulnerable)")

        module.run()

    def entry_to_module(self, module: Module) -> None:
        """ Prepare to entry the module.

        :param Module module: module object
        :return None: None
        :raises RuntimeError: with trailing error message
        """

        values = []

        for option in module.options:
            opt = module.options[option]
            val = str(opt['Value'])

            if val.startswith('file:') and len(val) > 5:
                file = val[5:]

                with open(file, 'r') as f:
                    vals = f.read().strip()
                    values.append(vals.split('\n'))

        if not values:
            self.run_module(module)
            return

        if not all(len(value) == len(values[0]) for value in values):
            raise RuntimeError("All files should contain equal number of values!")

        save = copy.deepcopy(module.options)
        for i in range(0, len(values[0])):
            count = 0

            for option in module.options:
                opt = module.options[option]
                val = str(opt['Value'])

                if val.startswith('file:') and len(val) > 5:
                    module.options[option]['Value'] = values[count][i]
                    count += 1

            try:
                self.run_module(module)
            except (KeyboardInterrupt, EOFError):
                pass

            module.options = save
            save = copy.deepcopy(module.options)

    def find_shorts(self, type: str, value: str) -> str:
        """ Find shorts by value, which is considered to be a number.

        :param str type: type of shorts, e.g. payload, encoder
        :param str value: value to search for in shorts
        :return str: found value in shorts
        """

        if type == 'payload':
            payload_shorts = self.local_storage.get("payload_shorts")

            if payload_shorts:
                if value.isdigit():
                    payload_number = int(value)

                    if payload_number in payload_shorts:
                        value = payload_shorts[payload_number]

        elif type == 'encoder':
            encoder_shorts = self.local_storage.get("encoder_shorts")

            if encoder_shorts:
                if value.isdigit():
                    encoder_number = int(value)

                    if encoder_number in encoder_shorts:
                        value = encoder_shorts[encoder_number]

        return value

    def get_current_options(self) -> dict:
        """ Get all options from current module,
        payload which is used in it and encoder.

        :return dict: options, option names as keys
        and option data as items
        """

        options = {}

        module = self.get_current_module()
        payload = self.payloads.get_current_payload(module)
        encoder = self.encoders.get_current_encoder(module, payload)

        if hasattr(module, 'options'):
            options.update(module.options)

        if hasattr(payload, 'options'):
            options.update(payload.options)

        if hasattr(encoder, 'options'):
            options.update(encoder.options)

        return options

    def get_current_advanced(self) -> dict:
        """ Get all advanced options from current module,
        payload which is used in it and encoder.

        :return dict: options, option names as keys
        and option data as items
        """

        options = {}

        module = self.get_current_module()
        payload = self.payloads.get_current_payload(module)
        encoder = self.encoders.get_current_encoder(module, payload)

        if hasattr(module, 'advanced'):
            options.update(module.advanced)

        if hasattr(payload, 'advanced'):
            options.update(payload.advanced)

        if hasattr(encoder, 'advanced'):
            options.update(encoder.advanced)

        return options

    def set_current_module_option(self, option: str, value: Optional[str] = None) -> None:
        """ Set current module option value.

        :param str option: option name
        :param Optional[str] value: value to set
        :return None: None
        :raises RuntimeWarning: with trailing warning message
        """

        module = self.get_current_module()
        payload = self.payloads.get_current_payload(module)
        encoder = self.encoders.get_current_encoder(module, payload)

        if not module:
            raise RuntimeWarning("No module selected.")

        if module.set(option, value):
            self.badges.print_information(f"{option} => {value}")
            return

        if payload and payload.set(option, value):
            self.badges.print_information(f"{option} => {value}")
            return

        if encoder and encoder.set(option, value):
            self.badges.print_information(f"{option} => {value}")
            return

        raise RuntimeError("Unrecognized option name!")

    def check_current_module(self) -> bool:
        """ Run check method on current module.

        :return bool: True if check succeed else False
        """

        module = self.get_current_module()

        if module:
            if hasattr(module, "check"):
                return module.check()

        return False

    def run_current_module(self, loop: bool = False, catch: Optional[Callable[..., None]] = None) -> None:
        """ Run current module.

        :param bool loop: run it in a loop
        :param Optional[Callable[..., None]] catch: function that catches Exceptions
        :return None: None
        """

        module = copy.deepcopy(self.get_current_module())

        payload = self.payloads.get_current_payload(module)
        encoder = self.encoders.get_current_encoder(module, payload)

        if module:
            module_name = module.details['Module']
            missed = self.options.validate_options(module)

            if payload:
                missed += self.options.validate_options(payload)

                if encoder:
                    missed += self.options.validate_options(encoder)

            if missed:
                raise RuntimeError(
                    f"These options are failed to validate: {', '.join(missed)}!")

            try:
                self.badges.print_empty()

                if loop:
                    while True:
                        if catch is not None:
                            catch(
                                self.entry_to_module, [module])
                        else:
                            self.entry_to_module(module)
                else:
                    if catch is not None:
                        catch(self.entry_to_module, [module])
                    else:
                        self.entry_to_module(module)

                self.badges.print_success(
                    f"{module_name.split('/')[0].title()} module completed!")

            except (KeyboardInterrupt, EOFError):
                raise RuntimeWarning(
                    f"{module_name.split('/')[0].title()} module interrupted.")

        else:
            raise RuntimeWarning("No module selected.")
