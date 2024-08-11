"""
MIT License

Copyright (c) 2020-2024 EntySec

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from textwrap import dedent


class Blocks(object):
    """ Subclass of pawn.windows.x64 module.

    This subclass of pawn.windows.x64 module contains API blocks
    for Windows.
    """

    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def x64_api_call() -> str:
        """ Get x64 API call.

        :return str: block
        """

        return dedent("""\
        api_call:
            push r9
            push r8
            push rdx
            push rcx
            push rsi
            xor  rdx, rdx
            mov  rdx, gs:[rdx+0x60]
            mov  rdx, [rdx+0x18]
            mov  rdx, [rdx+0x20]

        next_mod:
            mov   rsi, [rdx+0x50]
            movzx rcx, word ptr [rdx+0x4a]
            xor   r9, r9

        loop_modname:
            xor rax, rax
            lodsb
            cmp al, 'a'
            jl  not_lowercase
            sub al, 0x20

        not_lowercase:
            ror  r9d, 0xd
            add  r9d, eax
            loop loop_modname
            push rdx
            push r9
            mov  rdx, [rdx+0x20]
            mov  eax, dword ptr [rdx+0x3c]
            add  rax, rdx
            cmp  word ptr [rax+0x18], 0x020b
            jne  get_next_mod1
            mov  eax, dword ptr [rax+0x88]
            test rax, rax
            jz   get_next_mod1
            add  rax, rdx
            push rax
            mov  ecx, dword ptr [rax+0x18]
            mov  r8d, dword ptr [rax+0x20]
            add  r8, rdx

        get_next_func:
            jrcxz get_next_mod
            dec   rcx
            mov   esi, dword ptr [r8+rcx*0x4]
            add   rsi, rdx
            xor   r9, r9

        loop_funcname:
            xor rax, rax
            lodsb
            ror r9d, 0xd
            add r9d, eax
            cmp al, ah
            jne loop_funcname
            add r9, [rsp+0x8]
            cmp r9d, r10d
            jnz get_next_func
            pop rax
            mov r8d, dword ptr [rax+0x24]
            add r8, rdx
            mov cx, [r8+0x2*rcx]
            mov r8d, dword ptr [rax+0x1c]
            add r8, rax
            mov eax, dword ptr [r8+0x4*rcx]
            add rax, rdx

        finish:
            pop  r8
            pop  r8
            pop  rsi
            pop  rcx
            pop  rdx
            pop  r8
            pop  r9
            pop  r10
            sub  rsp, 0x20
            push r10
            jmp  rax

        get_next_mod:
            pop rax

        get_next_mod1:
            pop r9
            pop rdx
            mov rdx, [rdx]
            jmp next_mod
        """)
