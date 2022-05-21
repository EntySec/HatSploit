#!/usr/bin/env python3

#
# This module requires HatSploit: https://hatsploit.com
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.lib.module import Module
from hatsploit.lib.loot import Loot

from pex.assembler import Assembler


class HatSploitModule(Module, Assembler):
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
        executable, payload = self.payload['Executable'], self.payload['Payload']

        self.print_information(f"Payload size: {str(len(payload))}")
        self.print_information(f"Executable size: {str(len(executable))}")

        self.print_information(f"Payload hex view:")
        for line in self.hexdump(payload):
            self.print_empty(line)

        self.loot.save_file(path, executable)
