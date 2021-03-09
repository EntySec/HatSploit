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

import sys

from core.lib.command import HatSploitCommand

from core.base.jobs import jobs

class HatSploitCommand(HatSploitCommand):
    jobs = jobs()

    usage = ""
    usage += "exit [option]\n\n"
    usage += "    -h, --help   Show this help message.\n"
    usage += "    -f, --force  Force exit, ignoring active jobs."

    details = {
        'Category': "core",
        'Name': "exit",
        'Description': "Exit HatSploit Framework.",
        'Usage': usage,
        'MinArgs': 0
    }

    def run(self, argc, argv):
        if argc > 0:
            if argv[0] == "-f" or argv[0] == "--force":
                self.jobs.stop_all_jobs()
                sys.exit(0)
        if self.jobs.exit_jobs():
            sys.exit(0)
