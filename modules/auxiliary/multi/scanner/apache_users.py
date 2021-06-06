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
from utils.http import HTTPClient

from data.wordlists.apache_users_dictionary import Dictionary


class HatSploitModule(Module, HTTPClient):
    dictionary = Dictionary()
    paths = dictionary.paths

    details = {
        'Name': "Apache Users Scanner",
        'Module': "auxiliary/multi/scanner/apache_users",
        'Authors': [
            'Ivan Nikolsky (enty8080)'
        ],
        'Description': "Scan website apache users.",
        'Comments': [
            ''
        ],
        'Platform': "multi",
        'Risk': "medium"
    }

    options = {
        'RHOST': {
            'Description': "Remote host.",
            'Value': None,
            'Type': None,
            'Required': True
        },
        'RPORT': {
            'Description': "Remote port.",
            'Value': 80,
            'Type': "port",
            'Required': True
        },
        'SSL': {
            'Description': "Server has SSL certificate.",
            'Value': "no",
            'Type': "boolean",
            'Required': True
        }
    }

    def run(self):
        remote_host, remote_port, ssl = self.parse_options(self.options)
        ssl = ssl in ['yes', 'y']

        self.output_process(f"Scanning {remote_host}...")
        for path in self.paths:
            path = '/' + path.replace("\n", "")

            response = self.http_request(
                method="HEAD",
                host=remote_host,
                port=remote_port,
                path=path,
                ssl=ssl
            )

            if response is not None:
                if response.status_code == 200:
                    self.output_success("[%s] ... [%s %s]" % (path, response.status_code, response.reason))
                else:
                    self.output_warning("[%s] ... [%s %s]" % (path, response.status_code, response.reason))
