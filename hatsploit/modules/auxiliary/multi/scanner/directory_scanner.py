#!/usr/bin/env python3

#
# This module requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.base.module import Module
from hatsploit.base.config import Config
from hatsploit.utils.http import HTTPClient


class HatSploitModule(Module, HTTPClient):
    config = Config()

    details = {
        'Name': "Directory Scanner",
        'Module': "auxiliary/multi/scanner/directory_scanner",
        'Authors': [
            'Ivan Nikolsky (enty8080)'
        ],
        'Description': "Website directory scanner.",
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
        }
    }

    def run(self):
        remote_host, remote_port = self.parse_options(self.options)

        self.output_process(f"Scanning {remote_host}...")
        file = open(f"{self.config.path_config['data_path']}wordlists/directories.txt")
        directories = list(filter(None, file.read().split('\n')))
        file.close()

        for path in directories:
            path = '/' + path.replace("\n", "")

            response = self.http_request(
                method="HEAD",
                host=remote_host,
                port=remote_port,
                path=path
            )

            if response is not None:
                if response.status_code == 200:
                    self.output_success("[%s] ... [%s %s]" % (path, response.status_code, response.reason))
                else:
                    self.output_warning("[%s] ... [%s %s]" % (path, response.status_code, response.reason))
