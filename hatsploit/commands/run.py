"""
This command requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from badges.cmd import Command
from hatsploit.lib.ui.modules import Modules
from hatsploit.lib.ui.jobs import Jobs
from hatsploit.lib.runtime import Runtime
from hatsploit.lib.ui.sessions import Sessions


class ExternalCommand(Command):
    def __init__(self):
        super().__init__({
            'Category': "modules",
            'Name': "run",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - command developer',
            ],
            'Description': "Run current module.",
            'Usage': "run [option]",
            'MinArgs': 0,
            'Options': {
                'job': ['', "Run current module as a background job."],
                'cycle': ['', "Run current module in cycle."],
            },
        })

        self.modules = Modules()
        self.sessions = Sessions()
        self.runtime = Runtime()
        self.jobs = Jobs()

    def run(self, args):
        module = self.modules.get_current_module()

        if not module:
            self.print_warning("No module selected.")
            return

        if len(args) > 1 and args[1] == '-j':
            self.print_process("Running module as a background job...")

            self.sessions.disable_auto_interaction()
            self.print_warning("Disabled auto interaction with sessions.")

            job_id = self.jobs.count_jobs()

            if len(args) > 2 and args[2] == '-c':
                self.print_process("Requesting module to run in cycle...")

                self.jobs.create_job(
                    module.info['Name'],
                    module.info['Module'],
                    self.modules.run_current_module,
                    [True, self.runtime.catch],
                )

            else:
                self.jobs.create_job(
                    module.info['Name'],
                    module.info['Module'],
                    self.modules.run_current_module,
                    [False, self.runtime.catch],
                )

            self.print_information(
                f"Module started as a background job {str(job_id)}."
            )
        elif len(args) > 1 and args[1] == '-c':
            self.print_process("Requesting module to run in cycle...")

            self.sessions.disable_auto_interaction()
            self.print_warning("Disabled auto interaction with sessions.")

            if len(args) > 2 and args[2] == '-j':
                self.print_process("Running module as a background job...")

                job_id = self.jobs.count_jobs()

                self.jobs.create_job(
                    module.info['Name'],
                    module.info['Module'],
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
