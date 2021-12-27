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

from hatsploit.utils.fs import FSTools

from hatsploit.core.cli.badges import Badges
from hatsploit.core.session.pull.cat import Cat

from hatsploit.core.base.types import Types


class Pull(FSTools):
    badges = Badges()
    types = Types()

    pull_methods = {
        'cat': [
            types.platforms['unix'],
            Cat()
        ]
    }

    def pull(self, platform, file, sender, location, args=[], method=None):
        if method in self.pull_methods or not method:
            if not method:
                for pull_method in self.pull_methods:
                    if platform in self.pull_methods[pull_method][0]:
                        method = pull_method

                if not method:
                    self.badges.print_error("Failed to find supported pull method!")
                    return False
            else:
                if platform not in self.pull_methods[method][0]:
                    self.badges.print_error("Unsupported pull method!")
                    return False

            exists, is_dir = self.exists(location)
            if exists:
                if is_dir:
                    location = location + '/' + os.path.split(file)[1]

                self.badges.print_process(f"Downloading {file}...")
                data = self.pull_methods[method][1].pull(sender, file, args)

                if data:
                    self.badges.print_process(f"Saving to {location}...")
                    with open(location, 'wb') as f:
                        f.write(data)

                    self.badges.print_success(f"Saved to {location}!")
                    return True
                self.badges.print_error(f"Remote file: {file}: does not exist!")
                return False

            return False
        self.badges.print_error("Invalid pull method!")
        return False
