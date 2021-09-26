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

from hatsploit.lib.sessions import Sessions
from hatsploit.lib.storage import LocalStorage
from hatsploit.core.cli.badges import Badges
from hatsploit.lib.modules import Modules
from hatsploit.lib.jobs import Jobs
from hatsploit.lib.server import Server

from hatsploit.lib.session import Session
from hatsploit.utils.telnet import TelnetClient

from hatsploit.core.handler.stages.echo import EchoStage
from hatsploit.core.handler.stages.printf import PrintfStage
from hatsploit.core.handler.stages.wget import WgetStage

from hatsploit.core.handler.blinder import Blinder


class HatSploitSession(Session, TelnetClient):
    client = None

    details = {
        'Platform': "",
        'Type': "shell"
    }

    def open(self, client):
        self.client = self.open_telnet(client)

    def close(self):
        self.client.disconnect()

    def send_command(self, command, output=False, timeout=10):
        output = self.client.send_command(command + '\n', output, timeout)
        return output

    def interact(self):
        self.client.interact()


class Handler(Server):
    sessions = Sessions()
    local_storage = LocalStorage()
    modules = Modules()
    jobs = Jobs()
    badges = Badges()
    
    blinder = Blinder()

    def listen_session(self, local_host, local_port, timeout=None, session=HatSploitSession):
        try:
            client, address = self.listen(local_host, local_port, timeout)
            session = session()
            session.open(client)
            return session, address
        except Exception:
            self.badges.print_error("Failed to handle session!")
            return None, None

    def connect_session(self, remote_host, remote_port, timeout=None, session=HatSploitSession):
        try:
            client = self.connect(remote_host, remote_port, timeout)
            session = session()
            session.open(client)
            return session
        except Exception:
            self.badges.print_error("Failed to handle session!")
            return None

    def set_session_details(self, payload, session):
        if not session.details['Type']:
            session.details['Type'] = 'custom'

        session.details['Platform'] = payload['Platform']
        return session

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

    def raw_stage(self, payload, sender, args=[]):
        self.badges.print_process("Sending payload stage...")
        self.badges.print_process("Executing payload...")

        sender(*args, payload)

    def blinder(self, sender, args=[]):
        self.blinder.start(sender, args)

    def handle_session(self, host, port, payload, sender=None, args=[],
                       delim=';', remote_host=None, location='/tmp', timeout=10,
                       method=None, manual=False, post="printf", linemax=100):

        if payload['Payload'] is None:
            self.badges.print_error("Payload stage is not found!")
            return False

        if post.lower() != 'raw':
            if post.lower() not in self.stages:
                self.badges.print_error("Invalid post method selected!")
                return False

        else:
            if not payload['Raw']:
                self.badges.print_error("Payload does not support raw!")
                return False

        if sender is not None:
            session = payload['Session'] if payload['Session'] is not None else HatSploitSession

            if payload['Category'].lower() == 'stager':
                if post.lower() == 'raw':
                    self.do_job(
                        "Handler raw Stage",
                        payload,
                        self.raw_stage,
                        [
                            payload['Raw'],
                            sender,
                            args
                        ]
                    )
                else:
                    self.do_job(
                        f"Handler {post.lower()} Stage",
                        payload,
                        self.stages[post.lower()].send,
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
                    "Handler raw Stage",
                    payload,
                    self.raw_stage,
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
                    new_session, new_remote_host = self.listen_session(host, port, timeout, HatSploitSession)
                    if not new_session and not new_remote_host:
                        return False

                if method.lower() == 'bind_tcp':
                    new_session = self.connect_session(host, port, timeout, HatSploitSession)
                    new_remote_host = host
                    if not new_session:
                        return False

                if payload['Category'].lower() == 'stager':
                    if post.lower() == 'raw':
                        self.do_job(
                            "Handler raw Stage",
                            payload,
                            self.raw_stage,
                            [
                                payload['Raw'],
                                sender,
                                args
                            ]
                        )
                    else:
                        self.do_job(
                            f"Handler {post.lower()} Stage",
                            payload,
                            self.stages[post.lower()].send,
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
                        "Handler raw Stage",
                        payload,
                        self.raw_stage,
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
            new_session, new_remote_host = self.listen_session(host, port, timeout, session)
            if not new_session and not new_remote_host:
                return False

        if payload['Type'].lower() == 'bind_tcp':
            new_session = self.connect_session(host, port, timeout, session)
            new_remote_host = host
            if not new_session:
                return False

        if payload['Type'].lower() == 'one_side':
            self.badges.print_warning("Payload completed but no session was opened.")
            return True

        new_session = self.set_session_details(payload, new_session)
        session_platform = new_session.details['Platform']
        session_type = new_session.details['Type']

        if not remote_host:
            remote_host = new_remote_host
        session_id = self.sessions.add_session(session_platform, session_type, remote_host, port, new_session)
        self.badges.print_success("Session " + str(session_id) + " opened!")
        return True

    stages = {
        'echo': EchoStage(),
        'printf': PrintfStage(),
        'wget': WgetStage()
    }
