"""
This command requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.command import Command
from hatsploit.lib.modules import Modules
from hatsploit.lib.runtime import Runtime


class HatSploitCommand(Command):
    def __init__(self):
        super().__init__()

        self.modules = Modules()
        self.runtime = Runtime()

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

    def run(self, argc, argv):
        if argc > 1 and argv[1] == '-j':
            self.print_process("Running module as a background job...")

            if argc > 2 and argv[2] == '-c':
                self.print_process("Requesting module to run in cycle...")

                job_id = self.modules.run_current_module(job=True, cycle=True)

            else:
                job_id = self.modules.run_current_module(job=True)

            self.print_information(
                f"Module started as a background job {str(job_id)}."
            )
        elif argc > 1 and argv[1] == '-c':
            self.print_process("Requesting module to run in cycle...")

            self.modules.run_current_module(cycle=True)

        else:
            self.modules.run_current_module()
