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
import copy

from typing import (
    Any,
    Optional,
    Union,
    Callable
)


class Option(object):
    """ Subclass of hatsploit.lib module.

    This subclass of hatsploit.lib module is intended for providing
    an implementation of option for module, encoder and payload.
    """

    def __init__(self, name: str, value: Any = None,
                 description: Optional[str] = None,
                 required: bool = False, advanced: bool = False,
                 object: Any = None, conditions: dict = {}) -> None:
        """ Set option.

        :param str name: option name
        :param Any value: option value
        :param Optional[str] description: option description
        :param bool required: True if required else False
        :param bool advanced: True if advanced else False
        :param Any object: object
        :param dict conditions: add option only if other option
        has the value set to the value(s) specified in conditions
        :return None: None
        """

        super().__init__()

        self.name = name
        self.value = None

        self.description = description
        self.required = required

        self.advanced = advanced
        self.object = object
        self.conditions = conditions

        self.visible = True
        self.locked = False

        if value is not None:
            self.set(value)

    def __eq__(self, option: Any) -> bool:
        """ Check if option is equal to current one.

        :param Any option: can be option value or option
        :return bool: True if equal else False
        """

        if isinstance(option, self.__class__):
            if option.value == self.value:
                return True
        else:
            if option == self.value:
                return True

        return False

    @staticmethod
    def check(name: str, checker: Callable[[str], bool], value: Optional[str] = None) -> None:
        """ Compare value type using checker.

        :param str name: option name
        :param Callable[[str], bool] checker: checker function
        :param Optional[str] value: option value to check type for
        :return None: None
        :raises RuntimeError: with trailing error message
        """

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

    def set(self, value: Any) -> None:
        """ Set current option value.

        :param Any value: value
        :return None: None
        """

        if not self.locked:
            self.value = value

    def get(self) -> Any:
        """ Get current option value.

        :return Any: value
        """

        return self.value

    def unset(self) -> None:
        """ Unset current option value.

        :return None: None
        """

        self.value = None


class Options(object):
    """ Subclass of hatsploit.lib module.

    This subclass of hatsploit.lib module is intended for providing
    tools for working with module, payload or encoder options.
    """

    def get_option(self, option: str) -> Union[Option, None]:
        """ Get option object by name.

        :param str option: option name
        :return Union[Option, None]: option object or None
        """

        for name, object in self.options.items():
            if name.lower() != option.lower():
                continue

            return object

        for name, object in self.advanced.items():
            if name.lower() != option.lower():
                continue

            return object

    def set_option_attrs(self, option: str, attrs: dict) -> None:
        """ Set option attributes.

        :param str option: option name
        :param dict attrs: attrs to set
        :return None: None
        """

        option = self.get_option(option)

        if not option:
            return

        for attr, value in attrs.items():
            setattr(option, attr, value)

    def set(self, option: str, value: Optional[str] = None) -> bool:
        """ Set option.

        :param str option: option name
        :param Optional[str] value: option value
        :return bool: True if success else False
        """

        option = self.get_option(option)

        if not option:
            return False

        if not option.visible or option.locked:
            return False

        if value is not None:
            option.set(value)
        else:
            option.unset()

        self.update()
        return True

    def validate(self) -> list:
        """ Validate missed options.

        :return list: list of missed option names
        """

        missed = []

        for name, option in self.options.items():
            if not option.visible:
                continue

            if option.value is None and option.required:
                missed.append(name)

        return missed

    def update(self) -> None:
        """ Import external options from module, payload or encoder.

        NOTE: It also checks for conditions in the second part
        of the code.

        :return None: None
        """

        for attr in dir(self):
            option = getattr(self, attr)

            if not isinstance(option, Option):
                continue

            if option.object:
                if not isinstance(self, option.object):
                    continue

            if option.advanced:
                self.advanced[option.name] = option
                continue

            self.options[option.name] = option

        all_options = copy.deepcopy(self.options)
        all_options.update(self.advanced)

        for name in list(all_options):
            if name in self.options:
                option = self.options[name]
                options = self.options
            else:
                option = self.advanced[name]
                options = self.advanced

            if not option.conditions:
                continue

            for opt_name, opt_val in option.conditions.items():
                if opt_name not in all_options:
                    options.pop(name)
                    break

                if isinstance(opt_val, str):
                    if all_options[opt_name].value != opt_val:
                        options.pop(name)
                        break

                if isinstance(opt_val, list):
                    if all_options[opt_name].value not in opt_val:
                        options.pop(name)
                        break
