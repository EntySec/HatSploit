"""
This command requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from badges.cmd import Command
from hatsploit.lib.ui.jobs import Jobs
from hatsploit.lib.ui.show import Show


class ExternalCommand(Command):
    def __init__(self):
        super().__init__({
            'Category': "jobs",
            'Name': "jobs",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - command developer',
            ],
            'Description': "Manage active jobs.",
            'Usage': "jobs <option> [arguments]",
            'MinArgs': 1,
            'Options': {
                'list': ['', 'List all active jobs.'],
                'kill': ['<id>', 'Kill specified job.'],
            },
        })

        self.jobs = Jobs()
        self.show = Show()

    def run(self, args):
        if args[1] == 'list':
            self.show.show_jobs(self.jobs.get_jobs())

        elif args[1] == 'kill':
            self.jobs.delete_job(args[2])
