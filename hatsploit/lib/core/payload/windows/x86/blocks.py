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
    """ Subclass of pawn.windows.x86 module.

    This subclass of pawn.windows.x86 module contains API blocks
    for Windows.
    """

    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def x86_api_call() -> str:
        """ Get x86 API call.

        :return str: block
        """

        return dedent("""\
        api_call:
            pushad
            mov ebp, esp
            xor edx, edx
            mov edx, fs:[edx+0x30]
            mov edx, [edx+0xc]
            mov edx, [edx+0x14]

        next_mod:
            mov   esi, [edx+0x28]
            movzx ecx, word ptr [edx+0x26]
            xor   edi, edi

        loop_modname:
            xor eax, eax
            lodsb
            cmp al, 'a'
            jl  not_lowercase
            sub al, 0x20

        not_lowercase:
            ror  edi, 0xd
            add  edi, eax
            dec  ecx
            jnz  loop_modname
            push edx
            push edi
            mov  edx, [edx+0x10]
            mov  eax, [edx+0x3c]
            add  eax, edx
            mov  eax, [eax+0x78]
            test eax, eax
            jz   get_next_mod1
            add  eax, edx
            push eax
            mov  ecx, [eax+0x18]
            mov  ebx, [eax+0x20]
            add  ebx, edx

        get_next_func:
            test ecx, ecx
            jz   get_next_mod
            dec  ecx
            mov  esi, [ebx+ecx*4]
            add  esi, edx
            xor  edi, edi

        loop_funcname:
            xor eax, eax
            lodsb
            ror edi, 0xd
            add edi, eax
            cmp al, ah
            jne loop_funcname
            add edi, [ebp-8]
            cmp edi, [ebp+0x24]
            jnz get_next_func
            pop eax
            mov ebx, [eax+0x24]
            add ebx, edx
            mov cx, [ebx+2*ecx]
            mov ebx, [eax+0x1c]
            add ebx, edx
            mov eax, [ebx+4*ecx]
            add eax, edx

        finish:
            mov  [esp+0x24], eax
            pop  ebx
            pop  ebx
            popad
            pop  ecx
            pop  edx
            push ecx
            jmp  eax

        get_next_mod:
            pop eax

        get_next_mod1:
            pop edi
            pop edx
            mov edx, [edx]
            jmp next_mod
        """)
