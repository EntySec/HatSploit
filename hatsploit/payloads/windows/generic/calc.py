#!/usr/bin/env python3

#
# This payload requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.lib.payload import Payload


class HatSploitPayload(Payload):
    details = {
        'Category': "single",
        'Name': "Windows Calculator",
        'Payload': "windows/generic/calc",
        'Authors': [
            'Ivan Nikolsky (enty8080) - payload developer'
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
        self.output_process("Generating payload...")
        payload = "C:\Windows\System32\calc.exe"

        return payload
