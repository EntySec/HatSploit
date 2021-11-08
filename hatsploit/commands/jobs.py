#!/usr/bin/env python3

#
# This command requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.lib.command import Command
from hatsploit.lib.jobs import Jobs
from hatsploit.lib.show import Show


class HatSploitCommand(Command):
    jobs = Jobs()
    show = Show()

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
        choice = argv[1]
        if choice in ['-l', '--list']:
            self.show.show_jobs()

        elif choice in ['-k', '--kill']:
            if argc < 3:
                self.print_usage(self.details['Usage'])
            else:
                self.jobs.delete_job(argv[2])
        else:
            self.print_usage(self.details['Usage'])
