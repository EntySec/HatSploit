"""
This command requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.command import Command
from hatsploit.lib.modules import Modules
from hatsploit.lib.runtime import Runtime
from hatsploit.lib.jobs import Jobs
from hatsploit.lib.sessions import Sessions


class HatSploitCommand(Command):
    def __init__(self):
        super().__init__()

        self.modules = Modules()
        self.runtime = Runtime()
        self.sessions = Sessions()
        self.jobs = Jobs()

        self.details = {
            'Category': "modules",
            'Name': "run",
            'Authors': [
                'Ivan Nikolsky (enty8080) - command developer',
            ],
            'Description': "Run current module.",
            'Usage': "run [option]",
            'MinArgs': 0,
            'Options': {
                '-j': ['', "Run current module as a background job."],
                '-c': ['', "Run current module in cycle."],
            },
        }

    def loop(self):
        self.print_process("Requesting module to run in cycle...")

        self.modules.run_current_module(cycle=True)

    def run(self, argc, argv):
        current_module = self.modules.get_current_module()

        if argc > 1 and argv[1] == '-j':
            self.print_process("Running module as a background job...")
            job_id = self.jobs.count_jobs()

            if argc > 2 and argv[2] == '-c':
                self.jobs.create_job(
                    current_module.details['Name'],
                    current_module.details['Module'],
                    self.runtime.check,
                    [self.loop]
                )

            else:
                self.jobs.create_job(
                    current_module.details['Name'],
                    current_module.details['Module'],
                    self.runtime.check,
                    [self.modules.run_current_module]
                )

            self.print_information(
                f"Module started as a background job {str(job_id)}."
            )
        elif argc > 1 and argv[1] == '-c':
            if argc > 2 and argv[2] == '-j':
                self.print_process("Running module as a background job...")
                job_id = self.jobs.count_jobs()

                self.jobs.create_job(
                    current_module.details['Name'],
                    current_module.details['Module'],
                    self.runtime.check,
                    [self.loop]
                )

                self.print_information(
                    f"Module started as a background job {str(job_id)}."
                )
            else:
                self.loop()

        else:
            self.modules.run_current_module()
