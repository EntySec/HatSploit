#!/usr/bin/env python3

#
# This module requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.lib.module import Module


class HatSploitModule(Module):
    details = {
        'Name': "Multi Payload Generator",
        'Module': "auxiliary/multi/payload/generator",
        'Authors': [
            'Ivan Nikolsky (enty8080) - module developer'
        ],
        'Description': "Multi Payload Generator.",
        'Comments': [
            ''
        ],
        'Platform': "multi",
        'Risk': "high"
    }

    payload = {
        'Description': "Payload to use.",
        'Value': "linux/x64/shell_reverse_tcp",
        'Categories': None,
        'Architectures': None,
        'Platforms': None,
        'Types': None
    }

    options = {
        'RAW': {
            'Description': "Output raw payload.",
            'Value': "no",
            'Type': "boolean",
            'Required': False
        },
        'LPATH': {
            'Description': "Local path.",
            'Value': "/tmp/payload.bin",
            'Type': None,
            'Required': True
        }
    }

    def run(self):
        raw, local_file = self.parse_options(self.options)

        raw_payload = self.payload['Raw']
        payload = self.payload['Payload']

        if payload:
            self.print_process(f"Saving to {local_file}...")
            with open(local_file, 'wb') as f:
                if raw.lower() in ['yes', 'y']:
                    f.write(raw_payload.encode() if isinstance(raw_payload, str) else raw_payload)
                else:
                    f.write(payload.encode() if isinstance(payload, str) else payload)
            self.print_success(f"Successfully saved to {local_file}!")
        else:
            self.print_error("Failed to generate payload!")
