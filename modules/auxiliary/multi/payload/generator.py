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

from core.lib.module import Module


class HatSploitModule(Module):
    details = {
        'Name': "Multi Payload Generator",
        'Module': "auxiliary/multi/payload/generator",
        'Authors': [
            'enty8080'
        ],
        'Description': "Multi Payload Generator.",
        'Dependencies': [
            ''
        ],
        'Comments': [
            ''
        ],
        'Platform': "multi",
        'Risk': "high"
    }

    payload = {
        'Description': "Payload to use.",
        'Value': "linux/x64/shell_reverse_tcp",
        'Type': [
            'reverse_tcp',
            'bind_tcp',
            'one_side'
        ],
        'Category': [
            'stager',
            'single'
        ]
    }

    options = {
        'LPATH': {
            'Description': "Local path.",
            'Value': "/tmp/payload.bin",
            'Type': None,
            'Required': True
        }
    }

    def run(self):
        local_file = self.parse_options(self.options)
        payload = self.payload['Payload']

        if payload:
            self.output_process("Saving to " + local_file + "...")
            with open(local_file, 'wb') as f:
                f.write(payload.encode() if isinstance(payload, str) else payload)
            self.output_success("Successfully saved to " + local_file + "!")
