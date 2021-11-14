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
import json

from hatsploit.lib.session import Session
from hatsploit.lib.config import Config
from hatsploit.lib.commands import Commands

from hatsploit.utils.telnet import TelnetClient

class HatSploitSession(Session, TelnetClient):
    config = Config()
    commands = Commands()

    pwny = config.path_config['external_path'] + 'pwny/commands/'

    client = None
    terminated = False

    details = {
        'Platform': "",
        'Type': "pwny"
    }

    def open(self, client):
        self.client = self.open_telnet(client)

    def close(self):
        self.client.disconnect()

    def send_command(self, command, output=False, timeout=10):
        command = command.split()

        cmd = command[0]
        args = ""

        if len(command) > 1:
            args = ' '.join(command[1:])

        command_data = json.dumps({
            'cmd': cmd,
            'args': args
        })

        output = self.client.send_command(command_data, output, timeout)
        return output

    def interact(self):
        self.print_empty()

        if self.terminated:
            self.print_warning("Connection terminated.")
            return

        self.print_process("Loading Pwny commands...")
        commands = self.pwny + self.details['Platform'].lower()

        pwny = self.commands.load_commands(commands)
        for command in pwny:
            pwny[command].session = self

        self.print_information(f"Loaded {len(pwny)} commands.")
        self.print_empty()

        while True:
            commands = self.input_empty('%linepwny%end > ')

            if commands:
                if commands[0] == 'quit':
                    break

                elif commands[0] == 'help':
                    self.commands.show_commands(pwny)
                    continue

                self.commands.execute_custom_command(commands, pwny)

                if commands[0] == 'exit':
                    self.terminated = True
                    self.print_warning("Connection terminated.")
                    return
