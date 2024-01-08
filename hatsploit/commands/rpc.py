"""
This command requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.core.utils.rpc import RPC
from hatsploit.lib.command import Command
from hatsploit.lib.jobs import Jobs
from pex.proto.tcp import TCPTools


class HatSploitCommand(Command, TCPTools):
    def __init__(self):
        super().__init__()

        self.jobs = Jobs()

        self.details.update({
            'Category': "developer",
            'Name': "rpc",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - command developer',
            ],
            'Description': "Manage HatSploit RPC server.",
            'Usage': "rpc <option> [arguments]",
            'MinArgs': 1,
            'Options': {
                'off': ['<port>', "Turn RPC server off."],
                'on': ['<port>', "Turn RPC server on."],
            },
        })

    def run(self, argc, argv):
        if argv[1] == 'on':
            if not self.check_tcp_port('127.0.0.1', argv[2]):
                rpc = RPC(
                    host='127.0.0.1', port=argv[2]
                )

                self.print_success(f"RPC server started on port {argv[2]}!")
                self.jobs.create_job(f"RPC on port {argv[2]}", "", rpc.run)
            else:
                self.print_error(f"Failed to start RPC server!")

        elif argv[1] == 'off':
            pass
