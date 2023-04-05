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
import datetime

from typing import Optional, Callable, Tuple, Any, Union

from hatsploit.lib.blinder import Blinder
from hatsploit.lib.payload import Payload
from hatsploit.lib.module import Module
from hatsploit.lib.jobs import Jobs
from hatsploit.lib.encoders import Encoders
from hatsploit.lib.encoder import Encoder
from hatsploit.lib.sessions import Sessions
from hatsploit.lib.session import Session

from hatsploit.lib.handle import Handle

from hatsploit.lib.handler.hand import Hand
from hatsploit.lib.handler.misc import HatSploitSession

from hatsploit.core.cli.badges import Badges


class Handler(object):
    """ Main class of hatsploit.lib.handler module.

    This main class of hatsploit.lib.handler module is intended
    for providing tools for working with payloads and sessions.
    """

    def __init__(self) -> None:
        super().__init__()

        self.sessions = Sessions()
        self.hand = Hand()
        self.badges = Badges()
        self.jobs = Jobs()
        self.encoders = Encoders()

        self.blinder = Blinder()

        self.server_handle = Handle()

        self.actions = [
            'phaseless',
            'phase',
        ]

        self.types = [
            'one_side',
            'reverse_tcp',
            'bind_tcp'
        ]

    def open_session(self, host: str, port: int, session: Session,
                     on_session: Optional[Callable[..., Any]] = None) -> None:
        """ Open session and interact with it if allowed.

        Note: This method does not open session, it just saves opened session to the
        local storage and interacts with it if allowed.

        :param str host: session host
        :param int port: session port
        :param Session session: session object
        :param Optional[Callable[..., Any]] on_session: function of an action that
        should be performed right after session was opened
        :return None: None
        """

        platform = session.details['Platform']
        arch = session.details['Architecture']
        type = session.details['Type']

        session = self.sessions.add_session(platform, arch, type, host, port, session)
        time = datetime.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")

        self.badges.print_success(f"{type.title()} session {str(session)} opened at {time}!")

        if on_session:
            on_session()

        if self.sessions.get_auto_interaction:
            self.sessions.interact_with_session(session)

    def module_handle(self, module: Module, *args, **kwargs) -> None:
        """ Handle session from module.

        :param Module module: module object
        :return None: None
        :raises RuntimeError: with trailing error message
        """

        if not hasattr(module, "payload") or not hasattr(module, "handler"):
            raise RuntimeError("Module has not payload!")

        payload = module.payload['Payload']
        encoder = module.payload['Encoder']

        options = module.handler

        if 'BLINDER' in options:
            if options['BLINDER'].lower() in ['yes', 'y']:
                sender = kwargs.pop('sender', None)
                args = kwargs.pop('args', {})

                if sender:
                    return self.blinder.shell(sender, args)

        session = HatSploitSession

        if 'Session' in payload.details:
            session = payload.details['Session']

        action = module.payload['Action']
        actions = payload.details['Actions']

        if action not in actions:
            raise RuntimeError("Unresolved payload and module action conflict!")

        if payload.details['Type'] == 'bind_tcp':
            host = options['RBHOST']
            port = options['RBPORT']

        elif payload.details['Type'] == 'reverse_tcp':
            host = options['LHOST']
            port = options['LPORT']

        else:
            host, port = None, None

        self.handle(
            host=host,
            port=port,
            payload=payload,
            session=session,
            encoder=encoder,
            action=action,
            *args, **kwargs
        )

    def handle(self, payload: Payload, host: str, port: int, action: str,
               session: Optional[Session] = HatSploitSession, timeout: Optional[int] = None,
               encoder: Optional[Encoder] = None, on_session: Optional[Callable[..., Any]] = None,
               *args, **kwargs) -> None:
        """ Handle session.

        :param Payload payload: payload object
        :param str host: host
        :param int port: port
        :param str action: type of handler
        :param Optional[Session] session: session handler
        :param Optional[int] timeout: timeout
        :param Encoder encoder: encoder object of encoder to apply
        :param Optional[Callable[..., Any]] on_session: function of an action that
        should be performed right after session was opened
        """

        actions = payload.details['Actions']
        type = payload.details['Type']

        if actions and action not in actions:
            action = payload.details['Actions'][0]

        if action not in self.actions:
            raise RuntimeError(f"Unrecognized handler action: {action}!")

        if action == 'phaseless':
            self.jobs.create_job(
                job=None,
                module=None,
                target=self.hand.phaseless_payload,
                args=[payload, host, port, encoder, *args],
                kwargs=kwargs,
                hidden=True,
            )

        elif action == 'phase':
            self.jobs.create_job(
                job=None,
                module=None,
                target=self.hand.phase_payload,
                args=[payload, host, port, encoder, *args],
                kwargs=kwargs,
                hidden=True
            )

        client, host = self.hand.handle_session(host, port, type, session, timeout)

        if client:
            self.open_session(
                host=host,
                port=port,
                session=session,
                on_session=on_session
            )

    def module_handle_session(self, module: Module, type: str = 'one_side',
                              session: Optional[Session] = HatSploitSession,
                              timeout: Optional[int] = None) -> Tuple[Union[Session, socket.socket], str]:
        """ Handle session from module.

        :param Module module: module object
        :param str type: type of payload (see self.types)
        :param Optional[Session] session: session handler
        :param Optional[int] timeout: timeout
        :return Tuple[Union[Session, socket.socket], str]: session and host
        :raises RuntimeError: with trailing error message
        :raises RuntimeWarning: with trailing warning message
        """

        options = module.handler

        if type not in self.types:
            raise RuntimeError(f"Invalid payload type: {type}!")

        if type == 'reverse_tcp':
            return self.hand.handle_session(
                options['LHOST'], options['LPORT'], type, session, timeout)

        elif type == 'bind_tcp':
            return self.hand.handle_session(
                options['RBHOST'], options['RBPORT'], type, session, timeout)

        else:
            raise RuntimeWarning("Payload sent, but not session was opened.")
