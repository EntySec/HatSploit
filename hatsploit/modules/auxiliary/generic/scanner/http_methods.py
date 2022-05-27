#!/usr/bin/env python3

#
# This module requires HatSploit: https://hatsploit.com
# Current source: https://github.com/EntySec/HatSploit
#

import urllib.request
from urllib.error import HTTPError, URLError

from hatsploit.lib.module import Module


class HatSploitModule(Module):
    details = {
        'Category': 'auxiliary',
        'Name': 'HTTP Methods',
        'Module': 'auxiliary/generic/scanner/http_methods',
        'Authors': ['Noah Altunian (naltun) - contributor'],
        'Description': 'Find supported HTTP methods on a server',
        'Platform': 'generic',
        'Rank': 'low',
    }

    options = {
        'HOST': {
            'Description': 'Remote host.',
            'Value': None,
            'Type': 'ip',
            'Required': True,
        }
    }

    http_methods = [
        'CONNECT',
        'DELETE',
        'GET',
        'HEAD',
        'OPTIONS',
        'PATCH',
        'POST',
        'PUT',
        'TRACE',
    ]

    supported_methods = {'80': [], '443': []}

    def run(self):
        remote_host = self.parse_options(self.options)

        self.print_process(f'Scanning {remote_host}...')
        for method in self.http_methods:
            for port in [80, 443]:
                try:
                    req = urllib.request.Request(
                        url=f'http://{remote_host}:{port}', method=method
                    )
                    resp = urllib.request.urlopen(req)
                    if resp.status == 200:
                        self.supported_methods[str(port)].append(method)
                except (HTTPError, URLError):
                    continue

        if len(self.supported_methods['80']):
            self.print_success(
                f'Port 80 Supported Methods: {" ".join(self.supported_methods["80"])}'
            )
        if len(self.supported_methods['443']):
            self.print_success(
                f'Port 443 Supported Methods: {" ".join(self.supported_methods["443"])}'
            )
