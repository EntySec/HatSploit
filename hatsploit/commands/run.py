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

    usage = ""
    usage += "run [option]\n\n"
    usage += "  -h, --help  Show this help message.\n"
    usage += "  -j, --job   Run current module as a background job.\n"

    details = {
        'Category': "modules",
        'Name': "run",
        'Authors': [
            'Ivan Nikolsky (enty8080) - command developer'
        ],
        'Description': "Run current module.",
        'Usage': usage,
        'MinArgs': 0
    }

    def run(self, argc, argv):
        current_module = self.modules.get_current_module_object()

        if argc > 1:
            if argv[1] in ['-h', '--help']:
                self.print_usage(self.details['Usage'])
                return

            if argv[1] in ['-j', '--job']:
                job_id = self.jobs.create_job(current_module.details['Name'],
                                              current_module.details['Module'],
                                              self.modules.run_current_module)
                self.print_process("Running module as a background job...")
                self.print_information(f"Module started as a background job {str(job_id)}.")
                return

        self.modules.run_current_module()
