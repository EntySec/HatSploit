"""
This payload requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.core.payload.basic import *


class HatSploitPayload(Payload):
    def __init__(self):
        super().__init__({
            'Name': "Windows Message Box",
            'Payload': "windows/generic/message_box",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - payload developer',
            ],
            'Description': "Message Box payload for Windows.",
            'Arch': ARCH_GENERIC,
            'Platform': OS_WINDOWS,
            'Type': ONE_SIDE,
        })

        self.message = Option('MSG', "Hello, HatSploit!", "Message to show.", True)

    def run(self):
        source = (
            "[reflection.assembly]::loadwithpartialname('system.windows.forms');"
            f"[system.Windows.Forms.MessageBox]::show('{self.message.value}')"
        )

        payload = f"powershell -w hidden -nop -c {source}"
        return payload
