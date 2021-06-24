#!/usr/bin/env python3

#
# This module requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.base.module import Module
from hatsploit.utils.tcp import TCPClient


class HatSploitModule(Module, TCPClient):
    details = {
        'Name': "ADB Installation Checker",
        'Module': "auxiliary/android/checker/check_adb_installation",
        'Authors': [
            'Ivan Nikolsky (enty8080)'
        ],
        'Description': "Check if remote Android device has ADB installation.",
        'Comments': [
            ''
        ],
        'Platform': "android",
        'Risk': "low"
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

        self.output_process(f"Checking {remote_host}...")
        if self.check_tcp_port(remote_host, 5555):
            self.output_success("Target device may has ADB installation!")
        else:
            self.output_warning("Looks like target device has no ADB installation.")
