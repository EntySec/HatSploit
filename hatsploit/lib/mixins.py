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

from pex.type.dataset import DataSet


class PayloadMixin(DataSet):
    """ Subclass of hatsploit.lib.module.basic module.

    This subclass of hatsploit.lib.module.basic module is an implementation
    of a payload mixin set used to switch payload criteria.
    """

    def __init__(self,
                 inline: bool = False,
                 priority: bool = False,
                 force_defaults: bool = False,
                 *args, **kwargs) -> None:
        """ Initialize payload mixin.

        :param bool inline: payload can be sent as a stream of
        data without stages or dropping.
        :param bool priority: True to select over other payloads,
        else False
        :param bool force_defaults: use default mixin instead of current
        mixin
        :return None: None
        """

        super().__init__(*args, **kwargs)

        self.inline = inline
        self.priority = priority
        self.force_defaults = force_defaults


PayloadInlineMixin = PayloadMixin(
    name='Payload In-Line Mixin',
    inline=True,
    priority=False
)
PayloadDropMixin = PayloadMixin(
    name='Payload Dropper Mixin',
    inline=False,
    priority=True
)
PayloadGenericMixin = PayloadMixin(
    name='Payload Generic Mixin',
    force_defaults=True
)
