"""
This module requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.loot import Loot
from hatsploit.lib.module import Module
from hatsploit.lib.payloads import Payloads
from hatsploit.lib.encoders import Encoders

from pex.assembler import Assembler


class HatSploitModule(Module, Assembler):
    def __init__(self):
        super().__init__()

        self.loot = Loot()
        self.payloads = Payloads()

        self.details = {
            'Category': "auxiliary",
            'Name': "Generic Payload Generator",
            'Module': "auxiliary/generic/generator/payload",
            'Authors': [
                'Ivan Nikolsky (enty8080) - module developer',
            ],
            'Description': "Generate specified payload.",
            'Platform': "generic",
            'Rank': "low",
        }

        self.payload = {
            'Value': 'macos/x64/say',
            'Architectures': None,
            'Platforms': None,
            'Types': None,
        }

        self.options = {
            'PATH': {
                'Description': "Path to save file.",
                'Value': self.loot.random_loot(),
                'Type': None,
                'Required': True,
            }
        }

    def run(self):
        path = self.parse_options(self.options)
        payload = self.payload['Payload']

        executable = self.payloads.pack_payload(
            self.payloads.run_payload(
                payload,
                self.encoders.get_current_encoder(self, payload)
            ),
            payload.details['Platform'],
            payload.details['Architecture'],
        )

        self.loot.save_file(path, executable)
