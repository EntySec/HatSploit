"""
This command requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.command import Command
from hatsploit.lib.jobs import Jobs
from hatsploit.lib.show import Show


class HatSploitCommand(Command):
    def __init__(self):
        super().__init__()

        self.jobs = Jobs()
        self.show = Show()

        self.details.update({
            'Category': "jobs",
            'Name': "jobs",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - command developer',
            ],
            'Description': "Manage active jobs.",
            'Usage': "jobs <option> [arguments]",
            'MinArgs': 1,
            'Options': {
                '-l': ['', 'List all active jobs.'],
                '-k': ['<id>', 'Kill specified job.'],
            },
        })

    def run(self, argc, argv):
        choice = argv[1]

        if choice == '-l':
            self.show.show_jobs(self.jobs.get_jobs())

        elif choice == '-k':
            self.jobs.delete_job(argv[2])
