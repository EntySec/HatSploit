#!/usr/bin/env python3

#
# This payload requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

import struct

from hatvenom import HatVenom
from hatsploit.lib.payload import Payload


class HatSploitPayload(Payload, HatVenom):
    details = {
        'Category': "single",
        'Name': "Windows Say",
        'Payload': "windows/generic/say",
        'Authors': [
            'Ivan Nikolsky (enty8080) - payload developer'
        ],
        'Description': "Say payload for Windows.",
        'Comments': [
            ''
        ],
        'Architecture': "generic",
        'Platform': "windows",
        'Risk': "low",
        'Type': "one_side"
    }

    options = {
        'MESSAGE': {
            'Description': "Message to say.",
            'Value': "Hello, Friend!",
            'Type': None,
            'Required': True
        }
    }

    def run(self):
        message = self.parse_options(self.options)

        self.output_process("Generating payload...")
        payload = """
Function Invoke-VoiceTroll
{
    [CmdletBinding()]
    Param (
        [Parameter(Mandatory = $True, Position = 0)]
        [ValidateNotNullOrEmpty()]
        [String] $VoiceText
    )
    Set-StrictMode -version 2
    Add-Type -AssemblyName System.Speech
    $synth = New-Object -TypeName System.Speech.Synthesis.SpeechSynthesizer
    $synth.Speak($VoiceText)
}
Invoke-VoiceTroll"""

        return payload
