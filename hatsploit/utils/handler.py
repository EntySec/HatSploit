#!/usr/bin/env python3

#
# MIT License
#
# Copyright (c) 2020-2022 EntySec
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import datetime

from hatsploit.core.base.types import Types
from hatsploit.core.cli.badges import Badges

from hatsploit.core.session.handle import Handle
from hatsploit.core.session.post import Post
from hatsploit.core.session.blinder import Blinder

from hatsploit.core.session import HatSploitSession

from hatsploit.lib.jobs import Jobs
from hatsploit.lib.config import Config
from hatsploit.lib.modules import Modules
from hatsploit.lib.sessions import Sessions

from hatsploit.lib.storage import LocalStorage
from hatsploit.lib.storage import GlobalStorage


class Handler(Handle, Post, Blinder):
    sessions = Sessions()
    modules = Modules()
    jobs = Jobs()
    config = Config()
    types = Types()
    badges = Badges()

    storage_path = config.path_config['storage_path']

    global_storage = GlobalStorage(storage_path)
    local_storage = LocalStorage()

    def do_job(self, payload_type, target, args):
        if payload_type == 'one_side':
            target(*args)
        else:
            self.jobs.create_job(
                None,
                None,
                target,
                args,
                True
            )

    def ensure_linemax(self, payload, linemax):
        min_size = 10000
        max_size = 100000

        if len(payload) >= max_size and linemax not in range(min_size, max_size):
            self.badges.print_process(f"Ensuring payload size ({str(len(payload))} bytes)...")
            linemax = max_size

        return linemax

    def send(self, payload, sender, args=[]):
        if isinstance(payload, bytes):
            self.badges.print_process(f"Sending payload stage ({str(len(payload))} bytes)...")
        else:
            self.badges.print_process("Sending command payload stage...")

        if isinstance(args, dict):
            sender(payload, **args)
        else:
            sender(*args, payload)

    def open_session(self, host, port, session_platform, session_architecture, session_type, session):
        session_id = self.sessions.add_session(session_platform, session_architecture, session_type,
                                               host, port, session)
        time = datetime.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")

        self.badges.print_success(f"{session_type.title()} session {str(session_id)} opened at {time}!")

        if self.global_storage.get("interact"):
            self.sessions.spawn_interactive_connection(session_id)

    def module_handler(self, host=None, sender=None, args=[], concat=None, location=None,
                       background=None, method=None, timeout=None, linemax=100, ensure=False):
        module = self.modules.get_current_module_object()

        options = module.options
        payload = module.payload

        if 'BLINDER' in options:
            if options['BLINDER']['Value'].lower() in ['yes', 'y']:
                if sender is not None:
                    self.handler(
                        sender=sender,
                        args=args,
                        blinder=True
                    )

                    return True

        stage = payload['Payload'] if method != 'raw' else payload['Raw']

        if payload['Details']['Type'] == 'bind_tcp':
            port = options['RBPORT']['Value']

        elif payload['Details']['Type'] == 'reverse_tcp':
            host = options['LHOST']['Value']
            port = options['LPORT']['Value']

        else:
            host, port = None, None

        if 'Session' in payload['Details']:
            session = payload['Details']['Session']
        else:
            session = None

        platform = payload['Details']['Platform']
        architecture = payload['Details']['Architecture']

        if platform in self.types.platforms:
            module_platform = module.details['Platform']

            if module_platform not in self.types.platforms:
                platform = module_platform

        return self.handler(
            payload=stage,
            sender=sender,

            host=host,
            port=port,

            payload_category=payload['Details']['Category'],
            payload_type=payload['Details']['Type'],

            args=args,
            concat=concat,
            location=location,
            background=background,

            method=method,
            timeout=timeout,
            linemax=linemax,

            platform=platform,
            architecture=architecture,

            ensure=ensure,
            blinder=False,

            session=session
        )

    def handler(self, payload=None, sender=None, host=None, port=None, payload_category='stager',
                payload_type='one_side', args=[], concat=None, location=None, background=None,
                method=None, timeout=None, linemax=100, platform='generic', architecture='generic',
                ensure=False, blinder=False, session=None):

        if blinder:
            self.blinder(sender, args)
            return True

        if not self.send_payload(
            payload=payload,
            sender=sender,

            payload_category=payload_category,
            payload_type=payload_type,

            args=args,
            concat=concat,
            location=location,
            background=background,

            method=method,
            linemax=linemax,

            platform=platform,
            ensure=ensure
        ):
            self.badges.print_error("Failed to send payload stage!")
            return False

        remote = self.handle_session(
            host=host,
            port=port,

            payload_type=payload_type,
            session=session,
            timeout=timeout
        )

        if not remote:
            self.badges.print_warning("Payload sent but no session was opened.")
            return True

        session_type = remote[0].details['Type']

        remote[0].details['Post'] = method
        remote[0].details['Platform'] = platform
        remote[0].details['Architecture'] = architecture

        if remote[1] not in ('127.0.0.1', '0.0.0.0'):
            host = remote[1]

        self.open_session(host, port, platform, architecture, session_type, remote[0])
        return True

    def handle_session(self, host=None, port=None, payload_type='one_side', session=None, timeout=None):
        session = session if session is not None else HatSploitSession

        if payload_type == 'reverse_tcp':
            if not host or not port:
                return None

            new_session, host = self.listen_session(host, port, session, timeout)

            if not new_session and not host:
                return None

        elif payload_type == 'bind_tcp':
            if not host or not port:
                return None

            new_session = self.connect_session(host, port, session, timeout)

            if not new_session:
                return None

        elif payload_type == 'one_side':
            return None

        else:
            self.badges.print_error("Invalid payload type!")
            return None

        return new_session, host

    def send_payload(self, payload=None, sender=None, payload_category='stager', payload_type='one_side',
                     args=[], concat=None, location=None, background=None, method=None, linemax=100,
                     platform='generic', ensure=False):
        if payload is None:
            self.badges.print_error("Payload stage is not found!")
            return False

        if sender is None:
            self.badges.print_error("No sender found!")
            return False

        if ensure:
            linemax = self.ensure_linemax(payload['Payload'], linemax)

        if payload_category == 'stager':
            if method != 'raw':
                self.do_job(
                    payload_type,
                    self.post,
                    [
                        platform,
                        payload,
                        sender,
                        args,
                        method,
                        location,
                        concat,
                        background,
                        linemax
                    ]
                )

                return True

        if payload_category == 'single' or method == 'raw':
            self.do_job(
                payload_type,
                self.send,
                [
                    payload,
                    sender,
                    args
                ]
            )

        else:
            self.badges.print_error("Invalid payload category!")
            return False

        return True
