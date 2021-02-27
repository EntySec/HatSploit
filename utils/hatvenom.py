#!/usr/bin/env python3

#
# MIT License
#
# Copyright (c) 2020-2021 EntySec
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

class hatvenom:
    def __init__(self):
        self.formats = {
            'elf': self.generate_elf,
            'c': self.generate_c,
            'python': self.generate_python
        }

    #
    # Functions to convert data to bytes
    #
        
    def host_to_bytes(self, host):
        result = b""
        for i in host.split("."):
            result += bytes([int(i)])
        return result
        
    def port_to_bytes(self, port):
        result = "%.4x" % int(port)
        return bytes.fromhex(result)

    #
    # Functions to generate executable
    #
    
    def generate(file_format, arch, data):
        if file_format in self.formats.keys():
            return self.formats[file_format](arch, data)
        return None
