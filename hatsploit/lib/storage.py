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

import json

from typing import Union, Any
from badges import Badges


class GlobalStorage(object):
    """ Subclass of hatsploit.lib module.

    This subclass of hatsploit.lib module is intended for providing
    tools for interacting with global storage. Global storage represents
    storage which is storing data on the filesystem and does not reset
    after HatSploit exits.
    """

    def __init__(self, file: str) -> None:
        """ Initialize global storage.

        :param str file: name of file where you want to have
        global storage.
        :return None: None
        """

        super().__init__()

        self.file = file

    def set_all(self) -> None:
        """ Apply all variables from global storage.

        :return None: None
        """

        items = self.get_all()

        for key, item in items.items():
            if key == 'log':
                Badges().set_log(item)
            elif key == 'less':
                Badges().set_less(item)
            else:
                LocalStorage().set(key, item)

    def get_all(self) -> dict:
        """ Get all global storage variables as a dictionary.

        :return dict: variables, variable names as keys
        and variable values as items
        """

        return json.load(open(self.file))

    def set(self, variable: str, value: Any) -> None:
        """ Set global storage variable.

        :param str variable: variable name
        :param Any value: variable value
        :return None: None
        """

        config = self.get_all()
        config.update({variable: value})

        json.dump(config, open(self.file, 'w'))

    def get(self, variable: str) -> Union[None, Any]:
        """ Get global storage variable value.

        :param str variable: variable name
        :return Union[None, Any]: None if no such variable else value
        """

        storage_variables = self.get_all()

        if variable in storage_variables:
            return storage_variables[variable]

        return None

    def delete(self, variable: str) -> None:
        """ Delete global storage variable.

        :param str variable: variable name
        :return None: None
        """

        storage_variables = self.get_all()
        old_storage = storage_variables

        if variable in old_storage:
            new_storage = open(self.file, 'w')

            del old_storage[variable]
            new_storage.write(str(old_storage).replace("'", '"'))
            new_storage.close()
        else:
            pass


class LocalStorage(object):
    """ Subclass of hatsploit.lib module.

    This subclass of hatsploit.lib module is intended for providing
    tools for interacting and configuring local storage. Local storage
    is a general HatSploit storage that erases after HatSploit exits.
    """

    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def get_all() -> dict:
        """ Return all local storage variables.

        :return dict: variables, variable names as keys and
        variable values as items
        """

        return globals()

    @staticmethod
    def set(name: str, value: Any) -> None:
        """ Set local storage variable value.

        :param str name: variable name
        :param Any value: variable value
        :return None: None
        """

        globals()[name] = value

    def update(self, name: str, value: Any) -> None:
        """ Update local storage variable if it is a dictionary.

        :param str name: variable name
        :param Any value: variable value
        :return None: None
        """

        self.get(name, {}).update(value)

    def delete_element(self, name: str, value: str, default: Any = None) -> Any:
        """ Delete element from specific local storage variable
        if it is a dictionary.

        :param str name: variable name
        :param str value: value to delete
        :param Any default: value to return if element was not found
        :return Any: deleted element's value
        """

        return self.get(name, {}).pop(value, default)

    @staticmethod
    def delete(name: str, default: Any = None) -> Any:
        """ Delete variable from local storage.

        :param str name: variable name
        :param Any default: value to return if variable was not found
        :return Any: deleted variable's value
        """

        return globals().pop(name, default)

    @staticmethod
    def get(name: str, default: Any = None) -> Any:
        """ Get variable value from local storage.

        :param str name: variable name
        :param Any default: value to return if variable was not found
        :return Any: variable value
        """

        return globals().get(name, default)
