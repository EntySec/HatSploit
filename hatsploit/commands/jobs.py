#!/usr/bin/env python3

#
# This command requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.lib.command import Command
from hatsploit.lib.jobs import Jobs
from hatsploit.lib.storage import LocalStorage


class HatSploitCommand(Command):
    jobs = Jobs()
    local_storage = LocalStorage()

    usage = ""
    usage += "jobs <option> [arguments]\n\n"
    usage += "  -l, --list           List all active jobs.\n"
    usage += "  -k, --kill <job_id>  Kill specified job.\n"

    details = {
        'Category': "jobs",
        'Name': "jobs",
        'Authors': [
            'Ivan Nikolsky (enty8080) - command developer'
        ],
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
                self.print_table("Active Jobs", headers, *jobs_data)
            else:
                self.print_warning("No running jobs available.")
        elif choice in ['-k', '--kill']:
            if argc < 2:
                self.print_usage(self.details['Usage'])
            else:
                self.jobs.delete_job(argv[1])
        else:
            self.print_usage(self.details['Usage'])
