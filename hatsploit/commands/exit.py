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

    details = {
        'Category': "core",
        'Name': "exit",
        'Authors': [
            'Ivan Nikolsky (enty8080) - command developer'
        ],
        'Description': "Exit HatSploit Framework.",
        'Usage': "exit",
        'MinArgs': 0
    }

    def run(self, argc, argv):
        if self.jobs.exit_jobs() and self.sessions.close_sessions():
            sys.exit(0)
