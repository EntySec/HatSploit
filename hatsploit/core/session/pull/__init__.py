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

from hatsploit.utils.fs import FSTools

from hatsploit.core.session.pull.cat import Cat


class Pull(FSTools):
    pull_methods = {
        'cat': Cat()
    }

    def pull(self, remote_file, local_file, session, method=None):
        if not method:
            if session.details['Platform'] != 'windows':
                if session.details['Type'] == 'shell':
                    method = 'cat'
            else:
                method = 'powershell'

        if method in self.pull_methods:
            exists, is_dir = self.exists(local_file)
            if exists:
                if is_dir:
                    local_file = local_file + '/' + os.path.split(remote_file)[1]

                data = self.pull_methods[method].pull(remote_file, session)
                self.badges.print_process(f"Saving to {local_file}...")

                with open(local_file, 'wb') as file:
                    file.write(data)

                self.badges.print_success(f"File saved to {local_file}!")
        else:
            self.badges.print_error("Invalid pull method!")
