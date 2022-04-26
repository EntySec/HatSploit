#!/usr/bin/env python3

#
# This module requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.lib.module import Module
from hatsploit.lib.loot import Loot

from pex.assembler import AssemblerTools


class HatSploitModule(Module, AssemblerTools):
    loot = Loot()

    details = {
        'Category': "auxiliary",
        'Name': "Generic Payload Generator",
        'Module': "auxiliary/generic/generator/payload",
        'Authors': [
            'Ivan Nikolsky (enty8080) - module developer'
        ],
        'Description': "Generate specified payload.",
        'Platform': "generic",
        'Rank': "low"
    }

    payload = {
        'Value': 'macos/x64/say',
        'Categories': None,
        'Architectures': None,
        'Platforms': None,
        'Types': None
    }

    options = {
        'PATH': {
            'Description': "Path to save file.",
            'Value': loot.random_loot(),
            'Type': None,
            'Required': True
        }
    }

    def run(self):
        path = self.parse_options(self.options)
        payload, raw = self.payload['Payload'], self.payload['Raw']

        self.print_information(f"Payload size: {str(len(raw))}")
        self.print_information(f"Total payload size: {str(len(payload))}")

        self.print_information(f"Payload hex view:")
        for line in self.hexdump(raw):
            self.print_empty(line)

        self.loot.save_file(path, payload)
