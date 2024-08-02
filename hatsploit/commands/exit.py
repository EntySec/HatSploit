"""
This command requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

import sys

from badges.cmd import Command

from hatsploit.lib.ui.jobs import Jobs
from hatsploit.lib.ui.sessions import Sessions


class ExternalCommand(Command):
    def __init__(self):
        super().__init__({
            'Category': "core",
            'Name': "exit",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - command developer',
            ],
            'Description': "Exit HatSploit Framework.",
            'Usage': "exit",
            'MinArgs': 0,
        })

        self.jobs = Jobs()
        self.sessions = Sessions()

    def run(self, _):
        if self.jobs.get_jobs():
            self.print_warning("You have some running jobs.")

            if self.input_question("Exit anyway? [y/N] ").lower() in ['yes', 'y']:
                self.jobs.stop_jobs()
            else:
                return

        if self.sessions.get_sessions():
            self.print_warning("You have some opened sessions.")

            if self.input_question("Exit anyway? [y/N] ").lower() in ['yes', 'y']:
                self.sessions.close_sessions()
            else:
                return

        sys.exit(0)
