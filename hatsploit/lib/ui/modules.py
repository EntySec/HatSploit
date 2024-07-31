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

import sys
import traceback
import copy

from typing import Union, Optional, Callable

from badges import Badges

from hatsploit.core.db.importer import Importer

from hatsploit.lib.ui.payloads import Payloads
from hatsploit.lib.ui.sessions import Sessions
from hatsploit.lib.ui.encoders import Encoders

from hatsploit.lib.core.encoder import Encoder
from hatsploit.lib.core.payload import Payload
from hatsploit.lib.core.module import Module

from hatsploit.lib.storage import STORAGE


class Modules(Badges):
    """ Subclass of hatsploit.lib module.

    This subclass of hatsploit.lib module is intended for providing
    tools for working with HatSploit modules.
    """

    payloads = Payloads()
    encoders = Encoders()
    sessions = Sessions()

    def modules_completer(self) -> list:
        """ Tab-completion for modules.

        :return list: list of completions
        """

        modules = self.get_modules()
        complete = {}

        for database in modules:
            for module in modules[database]:
                complete[module] = None

        return complete

    @staticmethod
    def get_modules() -> dict:
        """ Get all modules from local storage.

        :return dict: modules, module names as keys and
        module objects as items
        """

        return STORAGE.get("modules", {})

    @staticmethod
    def get_imported_modules() -> dict:
        """ Get all imported modules from local storage.

        :return dict: modules, module name as keys and
        module objects as items
        """

        return STORAGE.get("imported_modules", {})

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
            imported_module = Importer().import_module(module_object['Path'])
            imported_module.update()

        except Exception:
            traceback.print_exc(file=sys.stdout)
            return None

        return imported_module

    def get_module_object(self, module: str) -> dict:
        """ Get module object, this object represents module details
        from the database.

        :param str module: module name
        :return dict: module object, module details
        """

        if not self.check_exist(module):
            return {}

        return self.get_modules()[
            self.get_database(module)][module]

    @staticmethod
    def get_current_module() -> Union[Module, None]:
        """ Get current module, this is module which is currently used.

        :return Union[Module, None]: current module, None if no current module
        """

        if STORAGE.get("current_module"):
            return STORAGE.get("current_module")[-1]

    @staticmethod
    def get_number_module(number: int) -> str:
        """ Get module name by its number.

        :param int number: module number
        :return str: module name
        """

        module = ''
        module_shorts = STORAGE.get("module_shorts")

        if module_shorts:
            if number in module_shorts:
                module = module_shorts[number]

        return module

    def search_module(self, name: str) -> str:
        """ Get module name by full module name.

        Note: Module name looks like this:
              - exploit/generic/handler
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

        if not module_object:
            return

        if self.get_imported_modules():
            STORAGE.update(
                "imported_modules", {module: module_object})
        else:
            STORAGE.set(
                "imported_modules", {module: module_object})

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

    @staticmethod
    def check_payload(module: Module) -> bool:
        """ Check if module has a payload configurable.

        :param Module module: module object
        :return bool: True if yes else False
        """

        return hasattr(module, 'payload')

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
            if module == current_module.info['Module']:
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
            return

        module_object = self.import_module(module)

        if not module_object:
            raise RuntimeError(f"Failed to select module from database: {module}!")

        self.add_to_global(module_object)

        if not self.set_current_module_target(0):
            if self.check_payload(module_object):
                module_object.payload.criteria.update(
                    module_object.info.get('Payload', {}))

        if self.check_payload(module_object):
            mixins = module_object.payload.criteria

            for mixin in mixins:
                payload_name = mixins[mixin].get('Value', None)

                if not mixin.priority:
                    continue

                if payload_name:
                    self.print_process(f"Using default payload {payload_name}...")

                    if not module_object.set('payload', payload_name):
                        self.go_back()
                        raise RuntimeError(f"Invalid default payload: {payload_name}!")

        module_object()
        module_object.update()

    def add_to_global(self, module: Module) -> None:
        """ Allocate space in local storage for module object.

        :param Module module: module object
        :return None: None
        """

        if self.get_current_module():
            current_module = STORAGE.get("current_module")
            current_module.append(module)

            STORAGE.set("current_module", current_module)
        else:
            STORAGE.set("current_module", [module])

    def go_back(self) -> None:
        """ Go back to the previous module in the local storage.

        :return None: None
        """

        if self.get_current_module():
            current_module = STORAGE.get("current_module")
            current_module.pop()

            STORAGE.set("current_module", current_module)

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
                f"{module.info['Category'].title()} module failed! (not vulnerable)")

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
            val = str(opt.value)

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
                val = str(opt.value)

                if val.startswith('file:') and len(val) > 5:
                    module.options[option].value = values[count][i]
                    count += 1

            try:
                self.run_module(module)
            except (KeyboardInterrupt, EOFError):
                pass

            module.options = save
            save = copy.deepcopy(module.options)

    @staticmethod
    def find_shorts(type: str, value: str) -> str:
        """ Find shorts by value, which is considered to be a number.

        :param str type: type of shorts, e.g. payload, encoder
        :param str value: value to search for in shorts
        :return str: found value in shorts
        """

        if type == 'payload':
            payload_shorts = STORAGE.get("payload_shorts")

            if payload_shorts:
                if value.isdigit():
                    payload_number = int(value)

                    if payload_number in payload_shorts:
                        value = payload_shorts[payload_number]

        elif type == 'encoder':
            encoder_shorts = STORAGE.get("encoder_shorts")

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

        if module:
            options.update(module.options)

        if payload:
            options.update(payload.options)

        if encoder:
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

        if module:
            options.update(module.advanced)

        if payload:
            options.update(payload.advanced)

        if encoder:
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
            self.print_information(f"{option} => {value}")
            return

        if payload and payload.set(option, value):
            self.print_information(f"{option} => {value}")
            return

        if encoder and encoder.set(option, value):
            self.print_information(f"{option} => {value}")
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

    def set_current_module_target(self, target_id: int) -> bool:
        """ Set current module target.

        :param int target_id: target ID
        :return bool: True if success else False
        :raises RuntimeWarning: with trailing warning message
        """

        module = self.get_current_module()

        if not module:
            raise RuntimeWarning("No module selected.")

        targets = module.info['Targets']

        if target_id < 0 or len(targets) <= target_id:
            return False

        target = list(targets)[target_id]
        module.target = targets[target]
        module.target.update({'Name': target})

        if not self.check_payload(module):
            return True

        if 'Payload' in module.target:
            module.payload.criteria.update(module.target['Payload'])
        else:
            module.payload.criteria.update(
                module.info.get('Payload', {}))

        module.payload.unset()
        return True

    def run_current_module(self, loop: bool = False, catch: Optional[Callable[..., None]] = None) -> None:
        """ Run current module.

        :param bool loop: run it in a loop
        :param Optional[Callable[..., None]] catch: function that catches Exceptions
        :return None: None
        """

        module = copy.deepcopy(self.get_current_module())

        payload = self.payloads.get_current_payload(module)
        encoder = self.encoders.get_current_encoder(module, payload)

        if not module:
            raise RuntimeWarning("No module selected.")

        module_name = module.info['Module']
        missed = module.validate()

        if payload:
            missed += payload.validate()

            if encoder:
                missed += encoder.validate()

        if missed:
            raise RuntimeError(
                f"These options are failed to validate: {', '.join(missed)}!")

        try:
            self.print_empty()

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

            self.print_success(
                f"{module_name.split('/')[0].title()} module completed!")

        except (KeyboardInterrupt, EOFError):
            raise RuntimeWarning(
                f"{module_name.split('/')[0].title()} module interrupted.")
