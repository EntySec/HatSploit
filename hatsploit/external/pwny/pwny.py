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

import json

from hatsploit.lib.config import Config
from hatsploit.utils.string import StringTools


class Pwny(StringTools):
    config = Config()

    pwny_path = config.path_config['external_path'] + 'pwny/resources/'
    payloads = {
        'iphoneos': {
            'aarch64': open(pwny_path + 'pwny.aarch64', 'rb').read()
        }
    }

    def get_payload(self, platform, arch):
        if platform in self.payloads:
            if arch in self.payloads[platform]:
                return self.payloads[platform][arch]
        return None

    def encode_args(self, connback_host, connback_port):
        connback_data = json.dumps({
            'host': connback_host,
            'port': connback_port
        })

        return self.base64_string(connback_data)
