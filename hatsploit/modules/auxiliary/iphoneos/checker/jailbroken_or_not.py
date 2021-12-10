#!/usr/bin/env python3

#
# This module requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.lib.module import Module
from hatsploit.utils.tcp import TCPClient


class HatSploitModule(Module, TCPClient):
    details = {
        'Name': "Jailbreak Installation Checker",
        'Module': "auxiliary/iphoneos/checker/jailbroken_or_not",
        'Authors': [
            'Ivan Nikolsky (enty8080) - module developer'
        ],
        'Description': "Check if remote iPhone jailbroken.",
        'Comments': [
            ''
        ],
        'Platform': "iphoneos",
        'Rank': "low"
    }

    options = {
        'RHOST': {
            'Description': "Remote host.",
            'Value': None,
            'Type': "ip",
            'Required': True
        }
    }

    def run(self):
        remote_host = self.parse_options(self.options)

        self.print_process(f"Checking {remote_host}")
        if self.check_tcp_port(remote_host, 22):
            self.print_success("Target device may be jailbroken!")
        else:
            self.print_warning("Looks like target device is not jailbroken.")
