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

    details = {
        'Category': "jobs",
        'Name': "jobs",
        'Authors': [
            'Ivan Nikolsky (enty8080) - command developer'
        ],
        'Description': "Manage active jobs.",
        'MinArgs': 1,
        'Options': {
            '-l': [0, '', 'List all active jobs.'],
            '-k': [1, '<id>', 'Kill specified job.']
        }
    }

    def run(self, argc, argv):
        choice = argv[1]
        if choice == '-l':
            self.show.show_jobs()

        elif choice == '-k':
            self.jobs.delete_job(argv[2])
