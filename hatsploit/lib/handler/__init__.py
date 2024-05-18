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
import datetime

from pex.proto.tcp import TCPTools

from typing import Optional, Callable, Tuple, Any, Union

from hatsploit.lib.option import *
from hatsploit.lib.complex import *
from hatsploit.lib.blinder import Blinder
from hatsploit.lib.payload import Payload
from hatsploit.lib.module import Module
from hatsploit.lib.jobs import Jobs
from hatsploit.lib.encoders import Encoders
from hatsploit.lib.encoder import Encoder
from hatsploit.lib.sessions import Sessions
from hatsploit.lib.session import Session

from hatsploit.lib.handler.send import Send
from hatsploit.lib.handler.misc import HatSploitSession

from badges import Badges


class Handler(object):
    """ Main class of hatsploit.lib.handler module.

    This main class of hatsploit.lib.handler module is intended
    for providing tools for working with payloads and sessions.
    """

    def __init__(self) -> None:
        super().__init__()

        self.send = Send()

        self.sessions = Sessions()
        self.badges = Badges()
        self.jobs = Jobs()
        self.encoders = Encoders()

        self.actions = [
            'shell',
            'memory',
        ]

        self.types = [
            'one_side',
            'reverse_tcp',
            'bind_tcp'
        ]

        self.payload = PayloadOption(None, "Payload to use.", True, object=Module)
        self.blinder = BooleanOption('no', "Start blind command injection.", False, object=Module)
        self.encoder = EncoderOption(None, "Encoder to use.", False, object=Payload)

        self.lhost = IPv4Option(TCPTools.get_local_host(), "Local host.", True, object=Module)
        self.lport = PortOption(8888, "Local port.", True, object=Module)

        self.rhost = IPv4Option(TCPTools.get_local_host(), "Remote host.", True, object=Payload)
        self.rport = PortOption(8888, "Remote port.", True, object=Payload)

        self.space = IntegerOption(2048, "Buffer space available.",
                                   False, advanced=True, object=Module)

    def open_session(self, session: Session,
                     on_session: Optional[Callable[..., Any]] = None) -> None:
        """ Open session and interact with it if allowed.

        Note: This method does not open session, it just saves opened session to the
        local storage and interacts with it if allowed.

        :param Session session: session object
        :param Optional[Callable[..., Any]] on_session: function of an action that
        should be performed right after session was opened
        :return None: None
        """

        platform = str(session.details['Platform'])
        arch = str(session.details['Arch'])
        type = session.details['Type']
        host = session.details['Host']
        port = session.details['Port']

        session = self.sessions.add_session(platform, arch, type, host, port, session)
        time = datetime.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")

        self.badges.print_success(f"{type.title()} session {str(session)} opened at {time}!")

        if on_session:
            on_session()

        if self.sessions.get_auto_interaction():
            self.sessions.interact_with_session(session)

    def module_handle(self, *args, **kwargs) -> None:
        """ Handle session from module.

        :return None: None
        :raises RuntimeError: with trailing error message
        """

        if not self.payload.value:
            raise RuntimeError("Module has not payload!")

        payload = self.payload.payload
        encoder = self.encoder.encoder

        if self.blinder.value:
            sender = kwargs.pop('sender', None)

            if sender:
                return Blinder().shell(sender)

        session = HatSploitSession

        if 'Session' in payload.details and payload.details['Session']:
            session = payload.details['Session']

        self.handle(
            payload=payload,
            session=session,
            encoder=encoder,
            *args, **kwargs
        )

    def handle(self, payload: Payload, action: str = 'shell',
               session: Optional[Session] = HatSploitSession,
               encoder: Optional[Encoder] = None, on_session: Optional[Callable[..., Any]] = None,
               *args, **kwargs) -> None:
        """ Handle session.

        :param Payload payload: payload object
        :param str action: type of handler
        :param Optional[Session] session: session handler
        :param Encoder encoder: encoder object of encoder to apply
        :param Optional[Callable[..., Any]] on_session: function of an action that
        should be performed right after session was opened
        """

        space = kwargs.get('space', self.space.value)

        if action == 'shell':
            client, host = self.send.shell_payload(
                payload=payload,
                host=self.lhost.value,
                port=self.lport.value,
                space=space,
                encoder=encoder,
                *args, **kwargs
            )

        elif action == 'memory':
            client, host = self.send.memory_payload(
                payload=payload,
                host=self.lhost.value,
                port=self.lport.value,
                space=space,
                encoder=encoder,
                *args, **kwargs
            )

        else:
            raise RuntimeError(f"Unrecognized handler action: {action}!")

        if client:
            session = session()

            session.details['Platform'] = payload.details['Platform']
            session.details['Arch'] = payload.details['Arch']
            session.details['Host'] = host
            session.details['Port'] = self.lport.value

            session.open(client)

            self.open_session(
                session=session,
                on_session=on_session
            )

    def module_handle_session(self, type: str = 'one_side',
                              *args, **kwargs) -> Tuple[Union[Session, socket.socket], str]:
        """ Handle session from module.

        :param str type: type of payload (see self.types)
        :return Tuple[Union[Session, socket.socket], str]: session and host
        :raises RuntimeError: with trailing error message
        :raises RuntimeWarning: with trailing warning message
        """

        if type not in self.types:
            raise RuntimeError(f"Invalid payload type: {type}!")

        return self.send.handle_session(
            host=self.lhost.value, port=self.lport.value, type=type, *args, **kwargs)
