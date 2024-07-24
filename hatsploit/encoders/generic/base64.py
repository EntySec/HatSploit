"""
This encoder requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from pex.string import String

from hatsploit.lib.core.encoder.basic import *


class HatSploitEncoder(Encoder):
    def __init__(self):
        super().__init__({
            'Name': "Base64 Encoder for Command",
            'Encoder': "generic/base64",
            'Authors': [
                "Ivan Nikolskiy (enty8080) - encoder developer",
            ],
            'Description': "Encode command with base64.",
            'Arch': ARCH_GENERIC,
        })

        self.shell = Option('SHELL', "/bin/sh", "Shell to execute.", True)

    def run(self):
        encoded_payload = String().base64_string(self.payload)
        return f'base64 --decode <<< {encoded_payload} | {self.shell.value}'
