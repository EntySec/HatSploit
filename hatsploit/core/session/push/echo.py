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

from hatsploit.core.cli.badges import Badges


class Echo:
    badges = Badges()

    def bytes_to_octal(self, bytes_obj):
        byte_octals = []
        for byte in bytes_obj:
            byte_octal = '\\0' + oct(byte)[2:]
            byte_octals.append(byte_octal)
        return ''.join(byte_octals)

    def push(self, data, sender, location, args=[], linemax=100):
        echo_stream = "echo -en '{}' >> {}"
        echo_max_length = linemax

        size = len(data)
        num_parts = int(size / echo_max_length) + 1

        for i in range(0, num_parts):
            current = i * echo_max_length
            block = self.bytes_to_octal(data[current:current + echo_max_length])
            if block:
                command = echo_stream.format(block, location)

                self.badges.print_multi(f"Uploading to {location}... ({str(current)}/{str(size)})")

                if isinstance(args, dict):
                    sender(command, **args)
                else:
                    sender(*args, command)
