#!/usr/bin/env python3

#
# This command requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.lib.command import Command
from hatsploit.lib.jobs import Jobs

from pex.proto.tcp import TCPClient

from hatsploit.core.utils.api import API


class HatSploitCommand(Command, TCPClient):
    jobs = Jobs()

    details = {
        'Category': "developer",
        'Name': "api",
        'Authors': [
            'Ivan Nikolsky (enty8080) - command developer'
        ],
        'Description': "Manage HatSploit REST API server.",
        'Usage': "api <option> [arguments]",
        'MinArgs': 1,
        'Options': {
            'off': ['<port>', "Turn REST API server off."],
            'on': ['<port> <username> <password>', "Turn REST API server on."]
        }
    }

    def run(self, argc, argv):
        if argv[1] == 'on':
            if not self.check_tcp_port('127.0.0.1', argv[2]):
                rest_api = API(
                    host='127.0.0.1',
                    port=argv[2],
                    username=argv[3],
                    password=argv[4]
                )

                self.print_success(f"REST API server started on port {argv[2]}!")

                self.print_information(f"Username: {rest_api.username}")
                self.print_information(f"Password: {rest_api.password}")
                self.print_information(f"API token: {rest_api.token}")

                self.jobs.create_job(
                    f"REST API on port {argv[2]}",
                    None,
                    rest_api.run
                )
            else:
                self.print_error(f"Failed to start REST API server!")

        elif argv[1] == 'off':
            pass
