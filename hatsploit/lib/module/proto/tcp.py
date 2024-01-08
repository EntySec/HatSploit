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

from pex.proto.tcp import TCPClient, TCPListener, TCPTools
from hatsploit.lib.option import *


class TCP(object):
    """ Subclass of hatsploit.lib.module.proto module.

    This subclass of hatsploit.lib.module.proto module is a representation
    of a wrapper of TCP client for a module.
    """

    def __init__(self) -> None:
        super().__init__()

        self.timeout = IntegerOption(10, "Connection timeout.", False)
        self.host = IPv4Option(None, "TCP host.", True)
        self.port = PortOption(None, "TCP port.", True)

    def is_on(self) -> bool:
        """ Check if TCP port is available.

        :return bool: True if TCP port is opened else False
        """

        return TCPTools().check_tcp_port(
            host=self.host.value,
            port=self.port.value,
            timeout=self.timeout.value
        )

    def open_tcp(self) -> TCPClient:
        """ Open TCP client.

        :return TCPClient: TCP client
        """

        return TCPClient(
            host=self.host.value,
            port=self.port.value,
            timeout=self.timeout.value
        )

    def listen_tcp(self) -> TCPListener:
        """ Start TCP listener.

        :return TCPListener: TCP listener
        """

        return TCPListener(
            host=self.host.value,
            port=self.port.value,
            timeout=self.timeout.value
        )
