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

from core.lib.command import HatSploitCommand

from core.base.payloads import payloads
from core.base.storage import local_storage
from core.modules.modules import modules
from core.base.jobs import jobs

class HatSploitCommand(HatSploitCommand):
    payloads = payloads()
    local_storage = local_storage()
    modules = modules()
    jobs = jobs()

    usage = ""
    usage += "run [option]\n\n"
    usage += "  -h, --help  Show this help message.\n"
    usage += "  -j, --job   Run current module as a background job.\n"

    details = {
        'Category': "module",
        'Name': "run",
        'Authors': [
            'enty8080'
        ],
        'Description': "Run current module.",
        'Usage': usage,
        'MinArgs': 0
    }

    def entry_to_module(self, argc, argv, current_module):
        if argc > 0:
            if argv[0] in ['-j', '--job']:
                self.badges.output_process("Running module as a background job...")
                job_id = self.jobs.create_job(current_module.details['Name'], current_module.details['Module'], current_module.run)
                self.badges.output_information("Module started as a background job " + str(job_id) + ".")
                return
        current_module.run()

    def run(self, argc, argv):
        if argc > 0:
            if argv[0] in ['-h', '--help']:
                self.badges.output_usage(self.details['Usage'])
                return

        if self.modules.check_current_module():
            current_module = self.modules.get_current_module_object()
            count = 0
            if hasattr(current_module, "options"):
                for option in current_module.options.keys():
                    current_option = current_module.options[option]
                    if not current_option['Value'] and current_option['Value'] != 0 and current_option['Required']:
                        count += 1
                if count > 0:
                    self.badges.output_error("Missed some required options!")
                else:
                    try:
                        self.entry_to_module(argc, argv, current_module)
                    except Exception as e:
                        self.badges.output_error("An error occurred in module: " + str(e) + "!")
            else:
                try:
                    self.entry_to_module(argc, argv, current_module)
                except Exception as e:
                    self.badges.output_error("An error occurred in module: " + str(e) + "!")
        else:
            self.badges.output_warning("No module selected.")
