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

from pex.proto.ftp import FTPClient, FTPSocket
from hatsploit.lib.option import *


class FTP(FTPClient):
    """ Subclass of hatsploit.lib.module.proto module.

    This subclass of hatsploit.lib.module.proto module is a representation
    of a wrapper of FTP client for a module.
    """

    def __init__(self) -> None:
        super().__init__()

        self.timeout = IntegerOption(10, "Connection timeout.", False)
        self.host = IPv4Option(None, "ADB host.", True)
        self.port = PortOption(23, "ADB port.", True)
        self.ssl = BooleanOption('no', "Use SSL.", False)

    def open_ftp(self) -> FTPSocket:
        """ Open FTP socket.

        :return FTPSocket: FTP socket
        """

        return super().open_ftp(
            host=self.host.value,
            port=self.port.value,
            timeout=self.timeout.value,
            ssl=self.ssl.value
        )
