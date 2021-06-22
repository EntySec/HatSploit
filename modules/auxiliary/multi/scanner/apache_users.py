#!/usr/bin/env python3

#
# This module requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.module import Module
from hatsploit.utils.http import HTTPClient

from data.wordlists.apache_users_dictionary import Dictionary


class HatSploitModule(Module, HTTPClient):
    dictionary = Dictionary()
    paths = dictionary.paths

    details = {
        'Name': "Apache Users Scanner",
        'Module': "auxiliary/multi/scanner/apache_users",
        'Authors': [
            'Ivan Nikolsky (enty8080)'
        ],
        'Description': "Scan website apache users.",
        'Comments': [
            ''
        ],
        'Platform': "multi",
        'Risk': "medium"
    }

    options = {
        'RHOST': {
            'Description': "Remote host.",
            'Value': None,
            'Type': None,
            'Required': True
        },
        'RPORT': {
            'Description': "Remote port.",
            'Value': 80,
            'Type': "port",
            'Required': True
        },
        'SSL': {
            'Description': "Server has SSL certificate.",
            'Value': "no",
            'Type': "boolean",
            'Required': True
        }
    }

    def run(self):
        remote_host, remote_port, ssl = self.parse_options(self.options)
        ssl = ssl in ['yes', 'y']

        self.output_process(f"Scanning {remote_host}...")
        for path in self.paths:
            path = '/' + path.replace("\n", "")

            response = self.http_request(
                method="HEAD",
                host=remote_host,
                port=remote_port,
                path=path,
                ssl=ssl
            )

            if response is not None:
                if response.status_code == 200:
                    self.output_success("[%s] ... [%s %s]" % (path, response.status_code, response.reason))
                else:
                    self.output_warning("[%s] ... [%s %s]" % (path, response.status_code, response.reason))
