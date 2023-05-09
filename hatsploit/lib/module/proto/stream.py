"""
MIT License

Copyright (c) 2020-2023 EntySec

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

from pex.proto.stream import StreamClient, Streamer
from hatsploit.lib.option import *


class Stream(StreamClient):
    """ Subclass of hatsploit.lib.module.proto module.

    This subclass of hatsploit.lib.module.proto module is a representation
    of a wrapper of stream client for a module.
    """

    def __init__(self) -> None:
        super().__init__()

        self.html = Option(None, "HTML path.", False, True)

    def open_stream(self, *args, **kwargs) -> Streamer:
        """ Get streamer.

        :return Streamer: streamer
        """

        return super().open_stream(
            path=self.html.value,
            *args, **kwargs
        )
