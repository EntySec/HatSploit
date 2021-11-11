#!/usr/bin/env python3

#
# This command requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

import sys

from hatsploit.lib.command import Command
from hatsploit.lib.jobs import Jobs
from hatsploit.lib.sessions import Sessions


class HatSploitCommand(Command):
    jobs = Jobs()
    sessions = Sessions()

    usage = ""
    usage += "exit [option]\n\n"
    usage += "  -h, --help   Show this help message.\n"
    usage += "  -f, --force  Force exit, ignoring active jobs and opened sessions.\n"

    details = {
        'Category': "core",
        'Name': "exit",
        'Authors': [
            'Ivan Nikolsky (enty8080) - command developer'
        ],
        'Description': "Exit HatSploit Framework.",
        'Usage': usage,
        'MinArgs': 0
    }

    def run(self, argc, argv):
        if argc > 1:
            if argv[1] in ['-f', '--force']:
                self.jobs.stop_all_jobs()
                self.sessions.close_all_sessions()
                sys.exit(0)
            elif argv[1] in ['-h', '--help']:
                self.print_usage(self.details['Usage'])
                return
        if self.jobs.exit_jobs() and self.sessions.close_sessions():
            sys.exit(0)
