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

import socket

from typing import Union, Tuple, Optional, Callable

from hatsploit.lib.session import Session

from pex.proto.http import HTTPListener
from pex.proto.tcp import TCPClient
from pex.proto.tcp import TCPListener

from badges import Badges


class Handle(object):
    """ Subclass of hatsploit.lib module.

    This subclass of hatsploit.lib module is intended for providing
    native implementations of http/tcp servers and clients.
    """

    def __init__(self) -> None:
        super().__init__()

        self.badges = Badges()

    def listen_server(self, local_host: str, local_port: int, methods: dict = {}) -> None:
        """ HTTP server.

        :param str local_host: local host to start server on
        :param int local_port: local port to start server on
        :param dict methods: allowed HTTP methods, names as keys and
        handlers as items
        :return None: None
        """

        listener = HTTPListener(local_host, local_port, methods)

        self.badges.print_process(f"Starting HTTP listener on port {str(local_port)}...")
        listener.listen()

        while True:
            listener.accept()

    def listen_session(self, local_host: str, local_port: int,
                       session: Optional[Callable[[], Session]] = None,
                       timeout: Optional[int] = None) -> Tuple[Union[Session, socket.socket], str]:
        """ TCP listener for specific session handler.

        :param str local_host: local host to start server on
        :param int local_port: local port to start server on
        :param Optional[Callable[[], Session]] session: session handler
        :param Optional[int] timeout: timeout for server
        :return Tuple[Union[Session, socket.socket], str]: received session and address
        """

        listener = TCPListener(local_host, local_port, timeout)

        self.badges.print_process(f"Starting TCP listener on port {str(local_port)}...")

        listener.listen()
        listener.accept()

        address = listener.address

        self.badges.print_process(
            f"Establishing connection ({address[0]}:{str(address[1])} -> {local_host}:{str(local_port)})...")
        listener.stop()

        if session:
            session = session()
            session.open(listener.client)
        else:
            session = listener.client

        return session, address[0]

    def connect_session(self, remote_host: str, remote_port: int,
                        session: Optional[Callable[[], Session]] = None,
                        timeout: Optional[int] = None) -> Union[Session, socket.socket]:
        """ Connect to server and receive session.

        :param str remote_host: remote host to connect to
        :param int remote_port: remote port to connect to
        :param Optional[Callable[[], Session]] session: session handler
        :param Optional[int] timeout: connection timeout
        :return Union[Session, socket.socket]: received session
        """

        client = TCPClient(remote_host, remote_port, timeout)

        self.badges.print_process(f"Connecting to {local_host}:{str(local_port)}...")
        client.connect()

        self.badges.print_process(
            f"Establishing connection (0.0.0.0:{str(remote_port)} -> {remote_host}:{str(remote_port)})...")

        if session:
            session = session()
            session.open(client.sock)
        else:
            session = client.sock

        return session
