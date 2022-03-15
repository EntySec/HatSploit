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

from collections import OrderedDict

from hatsploit.core.utils.fs import FSTools
from hatsploit.core.cli.badges import Badges

from hatsploit.core.session.push.echo import Echo
from hatsploit.core.session.push.bash_echo import BashEcho

from hatsploit.core.session.push.printf import Printf
from hatsploit.core.session.push.certutil import Certutil

from hatsploit.core.base.types import Types


class Push(FSTools):
    badges = Badges()
    types = Types()

    push_methods = OrderedDict({
        'printf': [
            types.platforms['unix'],
            Printf()
        ],
        'echo': [
            types.platforms['unix'],
            Echo()
        ],
        'bash_echo': [
            types.platforms['unix'],
            BashEcho()
        ],
        'certutil': [
            types.platforms['windows'],
            Certutil()
        ]
    })

    def push(self, platform, file, sender, location, args=[], method=None, linemax=100):
        if method in self.push_methods or not method:
            if not method:
                for push_method in self.push_methods:
                    if platform in self.push_methods[push_method][0]:
                        method = push_method

                if not method:
                    self.badges.print_error("Failed to find supported push method!")
                    return False
            else:
                if platform not in self.push_methods[method][0]:
                    self.badges.print_error("Unsupported push method!")
                    return False

            if self.exists_file(file):
                self.badges.print_process(f"Uploading {file}...")

                with open(file, 'rb') as f:
                    self.push_methods[method][1].push(f.read(), sender, location, args, linemax)

                self.badges.print_process(f"Saving to {location}...")
                self.badges.print_success(f"Saved to {location}!")
                return True

            return False
        self.badges.print_error("Invalid push method!")
        return False
