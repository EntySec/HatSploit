"""
This payload requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.payload.basic import *


class HatSploitPayload(Payload):
    def __init__(self):
        super().__init__()

        self.details.update({
            'Name': "Windows Say",
            'Payload': "windows/generic/say",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - payload developer',
            ],
            'Description': "Say payload for Windows.",
            'Arch': ARCH_GENERIC,
            'Platform': OS_WINDOWS,
            'Type': OneSide,
        })

        self.message = Option("Hello, HatSploit!", "Message to show.", True)

    def run(self):
        source = (
            "Add-Type -AssemblyName System.speech;"
            "$speak = New-Object System.Speech.Synthesis.SpeechSynthesizer;"
            f"$speak.Speak('{self.message.value}')"
        )

        payload = f"powershell -w hidden -nop -c {source}"
        return payload
