"""
This module requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.module.basic import *
from pex.proto.http import HTTPClient
from pex.proto.tcp import TCPTools


class HatSploitModule(HTTPClient, Module, TCPTools):
    def __init__(self):
        super().__init__()

        self.details = {
            'Category': 'auxiliary',
            'Name': 'HTTP Header',
            'Module': 'auxiliary/generic/scanner/http_header',
            'Authors': ['Noah Altunian (naltun) - contributor'],
            'Description': 'Retrieve HTTP headers from a server.',
            'Platform': 'generic',
            'Rank': 'low',
        }

        self.host = IPv4Option(None, "Remote host.", True)
        self.port = PortOption(80, "Remote port", True)

        self.http_methods = ['HEAD', 'GET']
        self.headers = {}

    def run(self):
        remote_host, remote_port = self.host.value, self.port.value

        self.print_process(f'Scanning {remote_host}...')
        if self.check_tcp_port(remote_host, remote_port):
            for method in self.http_methods:
                resp = self.http_request(
                    method=method,
                    host=remote_host,
                    port=remote_port,
                    path='/',
                )

                if resp.status_code != 405:
                    self.print_information(
                        f'Header retrieved with %bold{method}%end HTTP method...'
                    )
                    self.print_success('HTTP header:')
                    for header, content in resp.headers.items():
                        self.print_empty(f'%bold{header}%end: {content}')
                    break
        else:
            self.print_error(f'Could not connect to {remote_host}:{remote_port}')
