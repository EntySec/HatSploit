#!/usr/bin/env python3

#
# MIT License
#
# Copyright (c) 2020-2021 EntySec
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

from hatsploit.core.cli.badges import Badges

from hatsploit.core.session.handle import Handle
from hatsploit.core.session.post import Post
from hatsploit.core.session.blinder import Blinder

from hatsploit.core.session import HatSploitSession

from hatsploit.lib.jobs import Jobs
from hatsploit.lib.modules import Modules
from hatsploit.lib.sessions import Sessions
from hatsploit.lib.storage import LocalStorage


class Handler(Handle, Post, Blinder):
    sessions = Sessions()
    local_storage = LocalStorage()
    modules = Modules()
    jobs = Jobs()
    badges = Badges()

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

    def open_session(self, host, port, session_platform, session_type, session):
        session_id = self.sessions.add_session(session_platform, session_type, host, port, session)
        time = datetime.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")

        self.badges.print_success(f"{session_type.title()} session {str(session_id)} opened at {time}!")

    def module_handler(self, host=None, sender=None, args=[], delim=';', location='/tmp', post='printf',
                timeout=10, linemax=100, ensure=False):
        module = self.modules.get_current_module_object()

        options = module.options
        payload = module.payload

        blinder = False
        if 'BLINDER' in options:
            if options['BLINDER']['Value'].lower() in ['yes', 'y']:
                if sender is not None:
                    blinder = True

        stage = payload['Payload'] if post != 'raw' else payload['Raw']

        if payload['Type'] == 'bind_tcp':
            port = options['RBPORT']['Value']

        elif payload['Type'] == 'reverse_tcp':
            host = options['LHOST']['Value']
            port = options['LPORT']['Value']
            
        else:
            host, port = None, None

        platform = payload['Platform']
        if platform == 'unix':
            platform = module.details['Platform']

        return self.handler(stage, sender, host, port, payload['Category'], payload['Type'],
                            payload['Args'], delim, location, post, timeout, linemax, platform, ensure,
                            blinder, payload['Session'])

    def handler(self, payload, sender, host=None, port=None, payload_category='stager', payload_type='one_side',
                payload_args=[], args=[], delim=';', location='/tmp', post='printf', timeout=10, linemax=100,
                platform='unix', ensure=False, blinder=False, session=None):

        if not self.send_payload(payload, sender, args, payload_args, delim, location, post, payload_category,
                                 payload_type, linemax, blinder, ensure):
            self.badges.print_error("Failed to send payload stage!")
            return False

        remote = self.handle_session(host, port, payload_type, session, timeout)
        if not remote:
            self.badges.print_warning("Payload sent but no session was opened.")
            return True

        session_type = remote[0].details['Type']
        remote[0].details['Platform'] = platform

        self.open_session(host if host is not None else remote[1], port, platform, session_type, remote[0])
        return True

    def handle_session(self, host=None, port=None, payload_type='one_side', session=None, timeout=10):
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

    def send_payload(self, payload, sender, args=[], payload_args=[], delim=';',
                location='/tmp', post='printf', payload_category='stager', payload_type='one_side',
                linemax=100, blinder=False, ensure=False):
        if blinder:
            self.blinder(sender, args)
            return False

        if payload is None:
            self.badges.print_error("Payload stage is not found!")
            return False

        if post != 'raw':
            if post not in self.post_methods:
                self.badges.print_error("Invalid post method!")
                return False

        if ensure:
            linemax = self.ensure_linemax(payload['Payload'], linemax)

        if payload_category == 'stager':
            if post != 'raw':
                self.do_job(
                    payload_type,
                    self.post,
                    [
                        payload,
                        sender,
                        args,
                        payload_args,
                        post,
                        location,
                        delim,
                        linemax
                    ]
                )

        elif payload_category == 'single' or post == 'raw':
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
