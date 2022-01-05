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
from hatsploit.lib.modules import Modules
from hatsploit.lib.payloads import Payloads
from hatsploit.lib.sessions import Sessions
from hatsploit.lib.storage import LocalStorage

from hatsploit.utils.tcp import TCPClient


class Handler(Handle, Post, Blinder):
    sessions = Sessions()
    modules = Modules()
    payloads = Payloads()
    jobs = Jobs()
    types = Types()
    badges = Badges()
    local_storage = LocalStorage()

    handler_options = {
        'Module': {
            'BLINDER': {
                'Description': 'Use Blinder.',
                'Value': 'yes',
                'Type': "boolean",
                'Required': True
            },
            'PAYLOAD': {
                'Description': 'Payload to use.',
                'Value': None,
                'Type': "payload",
                'Required': False
            },
            'LHOST': {
                'Description': "Local host to listen on.",
                'Value': "0.0.0.0",
                'Type': "ip",
                'Required': True
            },
            'LPORT': {
                'Description': "Local port to listen on.",
                'Value': 8888,
                'Type': "port",
                'Required': True
            },
            'RBPORT': {
                'Description': "Remote bind port.",
                'Value': 8888,
                'Type': "port",
                'Required': True
            }
        },
        'Payload': {
            'CBHOST': {
                'Description': "Connect-back host.",
                'Value': TCPClient.get_local_host(),
                'Type': "ip",
                'Required': True
            },
            'CBPORT': {
                'Description': "Connect-back port.",
                'Value': 8888,
                'Type': "port",
                'Required': True
            },
            'BPORT': {
                'Description': "Bind port.",
                'Value': 8888,
                'Type': "port",
                'Required': True
            }
        }
    }

    def remove_options(self, target, options):
        for option in list(target.options):
            if option.lower() in options:
                target.options.pop(option)

    @staticmethod
    def check_options(target):
        if not hasattr(target, "options"):
            return False
        if not isinstance(target.options, dict):
            return False
        return True

    def add_handler_options(self):
        if self.modules.check_current_module():
            current_module = self.modules.get_current_module_object()

            if hasattr(current_module, "payload"):
                blinder_option = 'blinder'.upper()
                payload_option = 'payload'.upper()

                handler_options = self.handler_options
                saved_handler_options = self.local_storage.get("handler_options")

                if not saved_handler_options:
                    saved_handler_options = {
                        'Module': {
                        },
                        'Payload': {
                        }
                    }

                module = self.modules.get_current_module_name()
                current_payload = self.payloads.get_current_payload()

                if module not in saved_handler_options['Module']:
                    saved_handler_options['Module'][module] = handler_options['Module']

                if not self.check_options(current_module):
                    current_module.options = {}

                current_module.options.update(saved_handler_options['Module'][module])
                current_module.options[payload_option]['Value'] = current_module.payload['Value']

                if not current_payload:
                    current_module.options[blinder_option]['Value'] = 'yes'
                    current_module.options[blinder_option]['Required'] = True
                else:
                    current_module.options[blinder_option]['Value'] = 'no'
                    current_module.options[blinder_option]['Required'] = False

                if 'Blinder' in current_module.payload:
                    if not current_module.payload['Blinder']:
                        current_module.options.pop(blinder_option)

                if blinder_option in current_module.options and not current_payload:
                    if current_module.options[blinder_option]['Value'].lower() in ['yes', 'y']:
                        current_module.payload['Value'] = None

                        current_module.options[payload_option]['Value'] = None
                        current_module.options[payload_option]['Required'] = False
                    else:
                        current_module.options[payload_option]['Required'] = True
                else:
                    current_module.options[payload_option]['Required'] = True

                if current_payload:
                    payload = current_module.payload['Value']

                    if payload not in saved_handler_options['Payload']:
                        saved_handler_options['Payload'][payload] = handler_options['Payload']

                    if not self.check_options(current_payload):
                        current_payload.options = {}

                    current_payload.options.update(saved_handler_options['Payload'][payload])

                    if 'Handler' in current_module.payload:
                        special = current_module.payload['Handler']
                    else:
                        special = []

                    if current_payload.details['Type'] == 'reverse_tcp':
                        if 'bind_tcp' not in special:
                            self.remove_options(current_module, ['rbport'])
                            self.remove_options(current_payload, ['bport'])

                    elif current_payload.details['Type'] == 'bind_tcp':
                        if 'reverse_tcp' not in special:
                            self.remove_options(current_module, ['lhost', 'lport'])
                            self.remove_options(current_payload, ['cbhost', 'cbport'])

                    else:
                        if 'reverse_tcp' not in special:
                            self.remove_options(current_module, ['lhost', 'lport'])
                            self.remove_options(current_payload, ['cbhost', 'cbport'])

                        if 'bind_tcp' not in special:
                            self.remove_options(current_module, ['rbport'])
                            self.remove_options(current_payload, ['bport'])
                else:
                    self.remove_options(current_module, ['lhost', 'lport', 'rbport'])

                for option in current_module.options:
                    if option.lower() in ['lhost', 'lport', 'rbport', 'payload', 'blinder']:
                        saved_handler_options['Module'][module][option]['Value'] = current_module.options[option]['Value']

                current_module.handler = saved_handler_options['Module'][module]

                if current_payload:
                    for option in current_payload.options:
                        if option.lower() in ['cbhost', 'cbport', 'bport']:
                            saved_handler_options['Payload'][payload][option]['Value'] = current_payload.options[option]['Value']

                    current_payload.handler = saved_handler_options['Payload'][payload]

                self.local_storage.set("handler_options", saved_handler_options)

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

        if self.local_storage.get("auto_interaction"):
            self.sessions.interact_with_session(session_id)

    def module_handle(self, host=None, sender=None, args=[], concat=None, location=None,
                       background=None, method=None, timeout=None, linemax=100, ensure=False):
        module = self.modules.get_current_module_object()

        options = module.handler
        payload = module.payload

        if 'BLINDER' in options:
            if options['BLINDER']['Value'].lower() in ['yes', 'y']:
                if sender is not None:
                    self.handle(
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

        return self.handle(
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

    def handle(self, payload=None, sender=None, host=None, port=None, payload_category='stager',
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

    def module_handle_session(self, host=None, session=None, timeout=None):
        module = self.modules.get_current_module_object()

        options = module.handler
        session = session if session is not None else HatSploitSession

        if 'LHOST' in options and 'LPORT' in options:
            new_session, host = self.listen_session(
                options['LHOST']['Value'],
                options['LPORT']['Value'],
                session, timeout
            )

            if not new_session and not host:
                return None

        elif 'RBPORT' in options:
            new_session = self.connect_session(
                host,
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
