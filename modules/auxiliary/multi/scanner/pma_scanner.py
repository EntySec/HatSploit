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
import sys

from core.lib.module import HatSploitModule

from utils.http.http import http

from data.modules.auxiliary.multi.scanner.pma_scanner.dictionary import dictionary

class HatSploitModule(HatSploitModule):
    http = http()

    dictionary = dictionary()
    paths = dictionary.paths

    details = {
        'Name': "PMA Scanner",
        'Module': "auxiliary/multi/scanner/pma_scanner",
        'Authors': [
            'enty8080'
        ],
        'Description': "Scan website PHP My Admin.",
        'Dependencies': [
            ''
        ],
        'Comments': [
            ''
        ],
        'Platform': "multi",
        'Risk': "medium"
    }

    options = {
        'URL': {
            'Description': "Target URL address.",
            'Value': None,
            'Type': None,
            'Required': True
        }
    }

    def run(self):
        target_url = self.parser.parse_options(self.options)

        self.badges.output_process("Scanning " + target_url + "...")

        if not self.http.check_url_access(target_url):
            self.badges.output_error("Failed to scan!")
            return

        for path in self.paths:
            path = path.replace("\n", "")
            response = self.http.http_request(method="HEAD", url=target_url, path=path)

            if response.status_code == 200:
                self.badges.output_success("[%s] ... [%s %s]" % (path, response.status_code, response.reason))
            else:
                self.badges.output_warning("[%s] ... [%s %s]" % (path, response.status_code, response.reason))
