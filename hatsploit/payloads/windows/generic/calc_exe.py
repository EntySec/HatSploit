#!/usr/bin/env python3

#
# This payload requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.lib.payload import Payload
from hatsploit.utils.tcp import TCPClient


class HatSploitPayload(Payload, TCPClient):
    details = {
        'Category': "single",
        'Name': "Windows Calculator",
        'Payload': "windows/generic/calc_exe",
        'Authors': [
            'Ivan Nikolsky (enty8080)'
        ],
        'Description': "Windows calc.exe payload.",
        'Comments': [
            ''
        ],
        'Architecture': "generic",
        'Platform': "windows",
        'Risk': "high",
        'Type': "one_side"
    }

    def run(self):
        local_host, local_port = self.parse_options(self.options)

        self.output_process("Generating payload...")
        payload = "C:\Windows\System32\calc.exe"

        return payload
