#!/usr/bin/env python3

#
# This command requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.lib.command import Command
from hatsploit.lib.jobs import Jobs
from hatsploit.lib.modules import Modules


class HatSploitCommand(Command):
    modules = Modules()
    jobs = Jobs()

    details = {
        'Category': "modules",
        'Name': "run",
        'Authors': [
            'Ivan Nikolsky (enty8080) - command developer'
        ],
        'Description': "Run current module.",
        'Usage': "run [option]",
        'MinArgs': 0,
        'Options': {
            '-j': ['', "Run current module as a background job."]
        }
    }

    def run(self, argc, argv):
        current_module = self.modules.get_current_module_object()

        if argc > 1:
            if argv[1] == '-j' and current_module:
                job_id = self.jobs.count_jobs()

                self.print_process("Running module as a background job...")
                self.print_information(f"Module started as a background job {str(job_id)}.")

                self.jobs.create_job(current_module.details['Name'],
                                     current_module.details['Module'],
                                     self.modules.run_current_module)
                return

        self.modules.run_current_module()
