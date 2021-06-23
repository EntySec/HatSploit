#!/usr/bin/env python3

#
# This command requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

import sys

from hatsploit.core.base.jobs import Jobs
from hatsploit.command import Command


class HatSploitCommand(Command):
    jobs = Jobs()

    usage = ""
    usage += "exit [option]\n\n"
    usage += "  -h, --help   Show this help message.\n"
    usage += "  -f, --force  Force exit, ignoring active jobs.\n"

    details = {
        'Category': "core",
        'Name': "exit",
        'Authors': [
            'Ivan Nikolsky (enty8080)'
        ],
        'Description': "Exit HatSploit Framework.",
        'Usage': usage,
        'MinArgs': 0
    }

    def run(self, argc, argv):
        if argc > 0:
            if argv[0] in ['-f', '--force']:
                self.jobs.stop_all_jobs()
                sys.exit(0)
            elif argv[0] in ['-h', '--help']:
                self.output_usage(self.details['Usage'])
                return
        if self.jobs.exit_jobs():
            sys.exit(0)
