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

from typing import Any, Union

from badges import Badges, Tables


class Session(Badges, Tables):
    """ Subclass of hatsploit.lib module.

    This subclass of hatsploit.lib module is intended for providing
    wrapper for a session.
    """

    def __init__(self) -> None:
        super().__init__()

        self.details = {
            'Post': "",
            'Platform': None,
            'Arch': None,
            'Type': "",
            'Host': "",
            'Port': None
        }

    def open(self, client: Any) -> None:
        """ Open this session for client.

        :param Any client: client (preferred: socket.socket)
        :return None: None
        """

        pass

    def close(self) -> None:
        """ Close this session.

        :return None: None
        """

        pass

    def heartbeat(self) -> bool:
        """ Check this session's heartbeat.

        :return bool: True if alive else False
        """

        return False

    def send_command(self, command: str, output: bool = False) -> Union[None, str]:
        """ Send command to this session.

        :param str command: command to send
        :param bool output: True to wait for output else False
        :return Union[None, str]: None if output is False else output
        """

        return None

    def download(self, remote_file: str, local_path: str) -> bool:
        """ Download file from this session.

        :param str remote_file: file to download
        :param str local_path: path to save file
        :return bool: True if success else False
        """

        return False

    def upload(self, local_file: str, remote_path: str) -> bool:
        """ Upload file to this session.

        :param str local_file: file to uplaod
        :param str remote_path: path to save file
        :return bool: True if success else False
        """

        return False

    def interact(self) -> None:
        """ Interact with this session.

        :return None: None
        """

        pass
