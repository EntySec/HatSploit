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

import re
import random
import string

##############################################################
# Lempel-Ziv-Stac decompression
# BitReader and RingList classes
#
# Copyright (C) 2011  Filippo Valsorda - FiloSottile
# filosottile.wiki gmail.com - www.pytux.it
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see &lt;http://www.gnu.org/licenses/&gt;.
#
##############################################################

import collections


class BitReader:
    def __init__(self, data_bytes):
        self._bits = collections.deque()

        for byte in data_bytes:
            for n in range(8):
                self._bits.append(bool((byte >> (7 - n)) & 1))

    def getBit(self):
        return self._bits.popleft()

    def getBits(self, num):
        res = 0
        for i in range(num):
            res += self.getBit() << num - 1 - i
        return res

    def getByte(self):
        return self.getBits(8)

    def __len__(self):
        return len(self._bits)


class RingList:
    def __init__(self, length):
        self.__data__ = collections.deque()
        self.__full__ = False
        self.__max__ = length

    def append(self, x):
        if self.__full__:
            self.__data__.popleft()
        self.__data__.append(x)
        if self.size() == self.__max__:
            self.__full__ = True

    def get(self):
        return self.__data__

    def size(self):
        return len(self.__data__)

    def maxsize(self):
        return self.__max__

    def __getitem__(self, n):
        if n >= self.size():
            return None
        return self.__data__[n]


def LZSDecompress(data, window=RingList(2048)):
    reader = BitReader(data)
    result = ''

    while True:
        bit = reader.getBit()
        if not bit:
            char = reader.getByte()
            result += chr(char)
            window.append(char)
        else:
            bit = reader.getBit()
            if bit:
                offset = reader.getBits(7)
                if offset == 0:
                    # EOF
                    break
            else:
                offset = reader.getBits(11)

            lenField = reader.getBits(2)
            if lenField < 3:
                length = lenField + 2
            else:
                lenField <<= 2
                lenField += reader.getBits(2)
                if lenField < 15:
                    length = (lenField & 0x0f) + 5
                else:
                    lenCounter = 0
                    lenField = reader.getBits(4)
                    while lenField == 15:
                        lenField = reader.getBits(4)
                        lenCounter += 1
                    length = 15 * lenCounter + 8 + lenField
            for i in range(length):
                char = window[-offset]
                result += chr(char)
                window.append(char)

    return result, window


class StringTools:
    @staticmethod
    def extract_strings(binary_data):
        strings = re.findall("[^\x00-\x1F\x7F-\xFF]{4,}", binary_data)
        return strings

    @staticmethod
    def xor_string(string):
        result = ""
        for c in string:
            result += chr(ord(c) ^ len(string))
        return result

    @staticmethod
    def random_string(length=16, alphabet=string.ascii_letters + string.digits):
        return "".join(random.choice(alphabet) for _ in range(length))

    @staticmethod
    def lzs_decompress(data, window=RingList(2048)):
        result, window = LZSDecompress(data, window)
        return result
