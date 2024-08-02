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
import datetime

from typing import Optional, Union

from pex.fs import FS
from pex.string import String

from hatsploit.lib.config import Config


class Loot(object):
    """ Subclass of hatsploit.lib module.

    This subclass of hatsploit.lib module is intended for providing
    tools for working with loot collected by HatSploit.
    """

    def __init__(self, loot: Optional[str] = None,
                 data: Optional[str] = None) -> None:
        """ Initialize loot.

        :param Optional[str] loot: loot root path
        :param Optional[str] data: data root path
        :return None: None
        """

        self.loot = loot or Config().path_config['loot_path']
        self.data = data or Config().path_config['data_path']

    def create_loot(self) -> None:
        """ Create loot directory in workspace.

        :return None: None
        """

        if not os.path.isdir(self.loot):
            os.mkdir(self.loot)

    def specific_loot(self, filename: str) -> str:
        """ Return full path to the specific file
        from the loot directory.

        :param str filename: file name
        :return str: path to the file
        """

        return self.loot + filename

    def random_loot(self, extension: Optional[str] = None) -> str:
        """ Generate random loot path and add extension (if specified).

        :param Optional[str] extension: extension
        :return str: random loot path
        """

        filename = String.random_string(16)

        if extension:
            filename += '.' + extension

        return self.loot + filename

    @staticmethod
    def get_file(filename: str) -> bytes:
        """ Get specific file contents.

        :param str filename: file name
        :return bytes: file contents
        """

        FS.check_file(filename)

        with open(filename, 'rb') as f:
            return f.read()

    @staticmethod
    def save_file(location: str, data: bytes, extension: Optional[str] = None,
                  filename: Optional[str] = None) -> Union[str, None]:
        """ Save contents to specific location.

        :param str location: location
        :param bytes data: contents to save
        :param Optional[str] extension: file extension
        :param Optional[str] filename: file name
        :return Union[str, None]: path if success else None
        """

        exists, is_dir = FS.exists(location)

        if exists:
            if is_dir:
                if location.endswith('/'):
                    location += os.path.split(filename)[1] if filename else String.random_string(16)
                else:
                    location += '/' + os.path.split(filename)[1] if filename else String.random_string(16)

            if extension:
                if not location.endswith('.' + extension):
                    location += '.' + extension

            with open(location, 'wb') as f:
                f.write(data)

            return os.path.abspath(location)
        return None

    @staticmethod
    def remove_file(filename: str) -> None:
        """ Remove specific file.

        :param str filename: file name
        :return None: None
        """

        FS.check_file(filename)
        os.remove(filename)

    def get_loot(self, filename: str) -> bytes:
        """ Get specific loot contents.

        :param str filename: file name of loot
        :return bytes data: loot contents
        """

        filename = os.path.split(filename)[1]
        return self.get_file(self.loot + filename)

    def save_loot(self, filename: str, data: bytes) -> Union[str, None]:
        """ Save contents to loot directory.

        :param str filename: file name of loot
        :param bytes data: loot contents
        :return Union[str, None]: path if success else None
        """

        filename = os.path.split(filename)[1]
        return self.save_file(self.loot + filename, data)

    def remove_loot(self, filename: str) -> None:
        """ Remove specific loot from loot directory.

        :param str filename: file name of loot
        :return None: None
        """

        filename = os.path.split(filename)[1]
        self.remove_file(self.loot + filename)

    def get_data(self, filename: str) -> bytes:
        """ Get contents of file from data directory.

        :param str filename: file name
        :return bytes: data contents
        :raises RuntimeError: with trailing error message
        """

        if os.path.exists(self.data + filename):
            with open(self.data + filename, 'rb') as f:
                return f.read()
        else:
            raise RuntimeError("Invalid data given!")

    def list_loot(self) -> list:
        """ List all loots from loot directory.

        :return list: all loots from loot directory
        """

        loots = []

        for loot in os.listdir(self.loot):
            loots.append((loot, self.loot + loot, datetime.datetime.fromtimestamp(
                os.path.getmtime(self.loot + loot)).astimezone().strftime(
                "%Y-%m-%d %H:%M:%S %Z")))

        return loots
