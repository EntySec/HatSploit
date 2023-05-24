"""
This module requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.loot import Loot
from hatsploit.lib.module.basic import *
from hatsploit.lib.payloads import Payloads
from hatsploit.lib.encoders import Encoders

from pex.assembler import Assembler


class HatSploitModule(Module, Assembler):
    def __init__(self):
        super().__init__()

        self.loot = Loot()
        self.payloads = Payloads()

        self.details.update({
            'Category': "auxiliary",
            'Name': "Generic Payload Generator",
            'Module': "auxiliary/generic/generator/payload",
            'Authors': [
                'Ivan Nikolsky (enty8080) - module developer',
            ],
            'Description': "Generate specified payload.",
            'Platform': "generic",
            'Rank': "low",
            'Payload': {
                'Value': 'macos/x64/say',
            }
        })

        self.path = Option(self.loot.random_loot(), "Path to save file.", True)

    def run(self):
        path = self.path.value
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
