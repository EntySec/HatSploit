"""
This encoder requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from pex.arch import X86
from pex.string import String

from hatsploit.lib.encoder.basic import *


class HatSploitEncoder(Encoder, String, X86):
    def __init__(self):
        super().__init__()

        self.details.update({
            'Name': "x64 XOR Encoder",
            'Encoder': "x64/xor",
            'Authors': (
                'Ivan Nikolskiy (enty8080) - encoder developer',
            ),
            'Description': "Simple XOR encoder for x64.",
            'Arch': ARCH_X64,
        })

        self.key = Option("hatspl64", "8-byte key to encode.", True)

    def run(self):
        count = -1 * int((len(self.payload) - 1 / len(self.key.value)) + 1)

        decoder = (
                b"\x48\x31\xc9"
                b"\x48\x81\xe9"
                + self.pack_dword(count) +
                b"\x48\x8d\x05\xef\xff\xff\xff"
                b"\x48\xbb"
                + self.key.value.encode() +
                b"\x48\x31\x58\x27"
                b"\x48\x2d\xf8\xff\xff\xff"
                b"\xe2\xf4"
        )

        return decoder + self.xor_key_bytes(self.payload, self.key.value.encode())
