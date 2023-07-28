"""
This payload requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.payload.basic import *


class HatSploitPayload(Payload):
    def __init__(self):
        super().__init__()

        self.details.update({
            'Name': "Windows Message Box",
            'Payload': "windows/generic/message_box",
            'Authors': [
                'Ivan Nikolsky (enty8080) - payload developer',
            ],
            'Description': "Message Box payload for Windows.",
            'Arch': "generic",
            'Platform': "windows",
            'Rank': "low",
            'Type': "one_side",
        })

        self.message = Option("Hello, HatSploit!", "Message to show.", True)

    def run(self):
        source = (
            "[reflection.assembly]::loadwithpartialname('system.windows.forms');"
            f"[system.Windows.Forms.MessageBox]::show('{self.message.value}')"
        )

        payload = f"powershell -w hidden -nop -c {source}"
        return payload
