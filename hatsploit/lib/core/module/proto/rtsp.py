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

from hatsploit.lib.base import BaseMixin
from pex.proto.rtsp import RTSPClient

from hatsploit.lib.ui.option import (
    IPv4Option,
    PortOption,
    IntegerOption
)


class RTSP(BaseMixin):
    """ Subclass of hatsploit.lib.module.proto module.

    This subclass of hatsploit.lib.module.proto module is a representation
    of a wrapper of RTSP client for a module.
    """

    def __init__(self, info: dict = {}) -> None:
        """ Initialize RTSP mixin.

        :param dict info: mixin info
        :return None: None
        """

        super().__init__(info)

        self.timeout = IntegerOption('TIMEOUT', 10, "Connection timeout.", False)
        self.host = IPv4Option('HOST', None, "SSH host.", True)
        self.port = PortOption('PORT', 554, "SSH port.", True)

    def open_rtsp(self) -> RTSPClient:
        """ Open RTSP client.

        :return RTSPClient: RTSP client
        """

        return RTSPClient(
            host=self.host.value,
            port=self.port.value,
            timeout=self.timeout.value
        )
