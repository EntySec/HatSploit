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

from core.base.jobs import jobs
from core.base.storage import local_storage

class HatSploitCommand(HatSploitCommand):
    jobs = jobs()
    local_storage = local_storage()

    usage = ""
    usage += "jobs <option> [arguments]\n\n"
    usage += "  -l, --list           List all active jobs.\n"
    usage += "  -k, --kill <job_id>  Kill specified job.\n"

    details = {
        'Category': "jobs",
        'Name': "jobs",
        'Description': "Manage active jobs.",
        'Usage': usage,
        'MinArgs': 1
    }

    def run(self, argc, argv):
        choice = argv[0]
        if choice in ['-l', '--list']:
            if self.local_storage.get("jobs"):
                jobs_data = list()
                headers = ("ID", "Name", "Module")
                jobs = self.local_storage.get("jobs")
                for job_id in jobs.keys():
                    jobs_data.append((job_id, jobs[job_id]['job_name'], jobs[job_id]['module_name']))
                self.badges.output_empty("")
                self.tables.print_table("Active Jobs", headers, *jobs_data)
                self.badges.output_empty("")
            else:
                self.badges.output_warning("No running jobs available.")
        elif choice in ['-k', '--kill']:
            if argc < 2:
                self.badges.output_usage(self.details['Usage'])
            else:
                self.jobs.delete_job(argv[1])
        else:
            self.badges.output_usage(self.details['Usage'])
