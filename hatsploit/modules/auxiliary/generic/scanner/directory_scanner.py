"""
This module requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.config import Config
from hatsploit.lib.module.basic import *
from pex.proto.http import HTTPClient


class HatSploitModule(Module, HTTPClient):
    def __init__(self):
        super().__init__()

        self.config = Config()

        self.details.update({
            'Category': "auxiliary",
            'Name': "WEB Directory Scanner",
            'Module': "auxiliary/generic/scanner/directory_scanner",
            'Authors': [
                'Ivan Nikolsky (enty8080) - module developer',
            ],
            'Description': "Website directory scanner.",
            'Platform': "generic",
            'Rank': "medium",
        })

        self.host = IPv4Option(None, "Remote host.", True)
        self.port = PortOption(80, "Remote port", True)

    def run(self):
        self.print_process(f"Scanning {self.host.value}...")

        with open(
            f"{self.config.path_config['wordlists_path']}directories.txt"
        ) as file:
            directories = list(filter(None, file.read().split('\n')))

        for path in directories:
            path = '/' + path.replace("\n", "")

            response = self.http_request(
                method="HEAD", host=self.host.value, port=self.port.value, path=path
            )

            if response is not None:
                if response.status_code == 200:
                    self.print_success(
                        "[%s] ... [%s %s]"
                        % (path, response.status_code, response.reason)
                    )
                else:
                    self.print_warning(
                        "[%s] ... [%s %s]"
                        % (path, response.status_code, response.reason)
                    )
