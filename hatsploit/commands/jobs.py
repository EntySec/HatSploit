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
            'Category': "manage",
            'Name': "jobs",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - command developer',
            ],
            'Description': "Manage active jobs.",
            'MinArgs': 1,
            'Options': [
                (
                    ('-l', '--list'),
                    {
                        'help': "List all active jobs.",
                        'action': 'store_true'
                    }
                ),
                (
                    ('-k', '--kill'),
                    {
                        'help': "Kill active job by ID.",
                        'metavar': 'ID',
                        'type': int
                    }
                )
            ]
        })

        self.jobs = Jobs()
        self.show = Show()

    def run(self, args):
        if args.list:
            self.show.show_jobs(self.jobs.get_jobs())

        elif args.kill is not None:
            self.jobs.stop_job(args.kill)
