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

import os

from typing import Any, Optional, Union, Callable


class Option(object):
    """ Subclass of hatsploit.lib module.

    This subclass of hatsploit.lib module is intended for providing
    an implementation of option for module, encoder and payload.
    """

    def __init__(self, value: Any = None, description: Optional[str] = None,
                 required: bool = False, advanced: bool = False,
                 object: Any = None) -> None:
        """ Set option.

        :param Any value: option value
        :param Optional[str] description: option description
        :param bool required: True if required else False
        :param bool advanced: True if advanced else False
        :param Any object: object
        :return None: None
        """

        super().__init__()

        self.value = None

        self.description = description
        self.required = required

        self.advanced = advanced
        self.object = object

        self.payload = None
        self.encoder = None
        self.session = None

        self.little = b''
        self.big = b''

        self.visible = True

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

    def set(self, value):
        self.value = value

    def get(self):
        return self.value

    def unset(self):
        self.value = None


class Options(object):
    """ Subclass of hatsploit.lib module.

    This subclass of hatsploit.lib module is intended for providing
    tools for working with module, payload or encoder options.
    """

    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def set_option(object: Any,
                   option: str, value: Optional[str] = None) -> bool:
        """ Set option.

        :param Any object: object
        :param str option: option name
        :param Optional[str] value: option value
        :return bool: True if success else False
        """

        if hasattr(object, 'advanced'):
            if option in object.advanced:
                attr = getattr(object, option)

                if attr.visible:
                    if value is not None:
                        attr.set(value)
                        object.advanced[option]['Value'] = str(value)
                    else:
                        attr.unset()
                        object.advanced[option]['Value'] = None

                    return True

        if hasattr(object, 'options'):
            if option in object.options:
                attr = getattr(object, option)

                if attr.visible:
                    if value is not None:
                        attr.set(value)
                        object.options[option]['Value'] = str(value)
                    else:
                        attr.unset()
                        object.options[option]['Value'] = None

                    return True

        return False

    @staticmethod
    def add_options(object: Any) -> None:
        """ Import external options from module, payload or encoder.

        :param Any object: object
        :return None: None
        """

        for attr in dir(object):
            option = getattr(object, attr)

            if not isinstance(option, Option):
                continue

            if option.object:
                if not isinstance(object, option.object):
                    continue

            if option.advanced:
                if not hasattr(object, 'advanced'):
                    object.advanced = {}

                options = object.advanced
            else:
                if not hasattr(object, 'options'):
                    object.options = {}

                options = object.options

            options.update(
                {
                    attr.lower(): {
                        'Value': option.value,
                        'Description': option.description,
                        'Required': option.required,
                        'Visible': option.visible
                    }
                }
            )
