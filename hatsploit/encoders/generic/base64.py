"""
This encoder requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from pex.string import String

from hatsploit.lib.encoder.basic import *


class HatSploitEncoder(Encoder, String):
    def __init__(self):
        super().__init__()

        self.details.update({
            'Name': "Base64 Encoder for Command",
            'Encoder': "generic/base64",
            'Authors': [
                'Ivan Nikolsky (enty8080) - encoder developer',
            ],
            'Description': "Encode command with base64.",
            'Architecture': "generic",
        })

        self.shell = Option("$SHELL", "Shell to execute.", True)

    def run(self):
        encoded_payload = self.base64_string(self.payload)
        return f'base64 --decode <<< {encoded_payload} | {self.shell.value}'
