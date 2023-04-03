"""
This payload requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.payload import Payload


class HatSploitPayload(Payload):
    def __init__(self):
        super().__init__()

        self.details = {
            'Name': "Windows Message Box",
            'Payload': "windows/generic/message_box",
            'Authors': [
                'Ivan Nikolsky (enty8080) - payload developer',
            ],
            'Description': "Message Box payload for Windows.",
            'Architecture': "generic",
            'Platform': "windows",
            'Rank': "low",
            'Type': "one_side",
            'Actions': ['execute']
        }

        self.options = {
            'MESSAGE': {
                'Description': "Message to show.",
                'Value': "Hello, Friend!",
                'Type': None,
                'Required': True,
            }
        }

    def run(self):
        message = self.parse_options(self.options)

        source = (
            "[reflection.assembly]::loadwithpartialname('system.windows.forms');"
            f"[system.Windows.Forms.MessageBox]::show('{message}')"
        )

        payload = f"powershell -w hidden -nop -c {source}"
        return payload
