"""
This module requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.config import Config

from hatsploit.lib.core.module.basic import *
from hatsploit.lib.core.module.proto import HTTP


class HatSploitModule(Module, HTTP):
    def __init__(self):
        super().__init__({
            'Category': "auxiliary",
            'Name': "WEB Directory Scanner",
            'Module': "auxiliary/generic/scanner/directory_scanner",
            'Authors': [
                "Ivan Nikolskiy (enty8080) - module developer",
            ],
            'Description': "Website directory scanner.",
            'Platform': OS_GENERIC,
            'Rank': MEDIUM_RANK,
        })

        self.config = Config()

    def run(self):
        self.print_process(f"Scanning {self.host.value}...")

        with open(
            f"{self.config.path_config['wordlists_path']}directories.txt"
        ) as file:
            directories = list(filter(None, file.read().split('\n')))

        for path in directories:
            path = '/' + path.replace("\n", "")

            response = self.http_request(
                method="HEAD", path=path
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
