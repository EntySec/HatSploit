"""
This command requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.command import Command
from hatsploit.lib.modules import Modules
from hatsploit.lib.jobs import Jobs
from hatsploit.lib.runtime import Runtime
from hatsploit.lib.sessions import Sessions


class HatSploitCommand(Command):
    def __init__(self):
        super().__init__()

        self.modules = Modules()
        self.sessions = Sessions()
        self.runtime = Runtime()
        self.jobs = Jobs()

        self.details.update({
            'Category': "modules",
            'Name': "run",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - command developer',
            ],
            'Description': "Run current module.",
            'Usage': "run [option]",
            'MinArgs': 0,
            'Options': {
                '-j': ['', "Run current module as a background job."],
                '-c': ['', "Run current module in cycle."],
            },
        })

    def run(self, argc, argv):
        module = self.modules.get_current_module()

        if not module:
            self.print_warning("No module selected.")
            return

        if argc > 1 and argv[1] == '-j':
            self.print_process("Running module as a background job...")

            self.sessions.disable_auto_interaction()
            self.print_warning("Disabled auto interaction with sessions.")

            job_id = self.jobs.count_jobs()

            if argc > 2 and argv[2] == '-c':
                self.print_process("Requesting module to run in cycle...")

                self.jobs.create_job(
                    module.details['Name'],
                    module.details['Module'],
                    self.modules.run_current_module,
                    [True, self.runtime.catch],
                )

            else:
                self.jobs.create_job(
                    module.details['Name'],
                    module.details['Module'],
                    self.modules.run_current_module,
                    [False, self.runtime.catch],
                )

            self.print_information(
                f"Module started as a background job {str(job_id)}."
            )
        elif argc > 1 and argv[1] == '-c':
            self.print_process("Requesting module to run in cycle...")

            self.sessions.disable_auto_interaction()
            self.print_warning("Disabled auto interaction with sessions.")

            if argc > 2 and argv[2] == '-j':
                self.print_process("Running module as a background job...")

                job_id = self.jobs.count_jobs()

                self.jobs.create_job(
                    module.details['Name'],
                    module.details['Module'],
                    self.modules.run_current_module,
                    [True, self.runtime.catch]
                )

                self.print_information(
                    f"Module started as a background job {str(job_id)}."
                )
            else:
                self.modules.run_current_module(loop=True)

        else:
            self.modules.run_current_module()
