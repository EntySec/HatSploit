#!/usr/bin/env python3

#
# This module requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.lib.config import Config
from hatsploit.lib.module import Module
from pex.proto.http import HTTPClient


class HatSploitModule(Module, HTTPClient):
    config = Config()

    details = {
        'Category': "auxiliary",
        'Name': "WEB Directory Scanner",
        'Module': "auxiliary/generic/scanner/directory_scanner",
        'Authors': [
            'Ivan Nikolsky (enty8080) - module developer'
        ],
        'Description': "Website directory scanner.",
        'Platform': "generic",
        'Rank': "medium"
    }

    options = {
        'HOST': {
            'Description': "Remote host.",
            'Value': None,
            'Type': None,
            'Required': True
        },
        'PORT': {
            'Description': "Remote port.",
            'Value': 80,
            'Type': "port",
            'Required': True
        }
    }

    def run(self):
        remote_host, remote_port = self.parse_options(self.options)

        self.print_process(f"Scanning {remote_host}...")

        with open(f"{self.config.path_config['wordlists_path']}directories.txt") as file:
            directories = list(filter(None, file.read().split('\n')))

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
                    self.print_success("[%s] ... [%s %s]" % (path, response.status_code, response.reason))
                else:
                    self.print_warning("[%s] ... [%s %s]" % (path, response.status_code, response.reason))
