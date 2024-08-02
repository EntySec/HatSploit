"""
This command requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from badges.cmd import Command
from hatsploit.lib.ui.jobs import Jobs
from hatsploit.core.utils.rpc import RPC
from pex.proto.tcp import TCPTools


class ExternalCommand(Command):
    def __init__(self):
        super().__init__({
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

        self.jobs = Jobs()

    def run(self, args):
        if args[1] == 'on':
            if not TCPTools().check_tcp_port('127.0.0.1', args[2]):
                rpc = RPC(
                    host='127.0.0.1', port=args[2]
                )

                self.print_success(f"RPC server started on port {args[2]}!")
                self.jobs.create_job(f"RPC on port {args[2]}", "", rpc.run)
            else:
                self.print_error(f"Failed to start RPC server!")

        elif args[1] == 'off':
            pass
