#!/usr/bin/env python3

#
# This module requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.lib.module import Module


class HatSploitModule(Module):
    details = {
        'Category': "auxiliary",
        'Name': "Test Module",
        'Module': "auxiliary/framework/tester/test",
        'Authors': [
            'Ivan Nikolsky (enty8080) - module developer'
        ],
        'Description': "Test module functionality.",
        'Platform': "framework",
        'Rank': "low"
    }

    options = {
        'OPTION': {
            'Description': "Test option.",
            'Value': None,
            'Type': None,
            'Required': True
        }
    }

    def run(self):
        option = self.parse_options(self.options)
        self.print_success(option)
