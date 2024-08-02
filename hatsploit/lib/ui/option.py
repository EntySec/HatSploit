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

import socket
from typing import Union

from pex.type import Type
from pex.socket import Socket

from hatsploit.lib.ui.options import Option


class BytesOption(Option):
    """ Subclass of hatsploit.lib.option module.

    This subclass of hatsploit.lib.option module is a representation
    of an option that stores bytes.
    """

    def set(self, value: bytes) -> None:
        """ Set current option value.

        :param bytes value: option value to set
        :return None: None
        """

        self.value = bytes.fromhex(value.replace('\\x', ''))


class IPv4Option(Option):
    """ Subclass of hatsploit.lib.option module.

    This subclass of hatsploit.lib.option module is a representation
    of an option that stores IPv4.
    """

    def __init__(self, *args, **kwargs) -> None:
        """ Initialize IPv4 option.

        :return None: None
        """

        self.big = b''
        self.little = b''

        super().__init__(*args, **kwargs)

    def __getattribute__(self, item):
        attr = super().__getattribute__(item)

        if attr is None:
            return

        if item == 'value':
            if Type.is_ipv4(attr):
                return attr

            return socket.gethostbyname(attr)

        elif item == 'little':
            attr = self.value

            if Type.is_ipv4(attr):
                return Socket().pack_host(attr)

            return Socket().pack_host(
                socket.gethostbyname(attr))

        elif item == 'big':
            attr = self.value

            if Type.is_ipv4(attr):
                return Socket().pack_host(attr, 'big')

            return Socket().pack_host(
                socket.gethostbyname(attr), 'big')

        return attr

    def set(self, value: str) -> None:
        """ Set current option value.

        :param str value: option value to set
        :return None: None
        """

        self.value = value


class IPv6Option(Option):
    """ Subclass of hatsploit.lib.option module.

    This subclass of hatsploit.lib.option module is a representation
    of an option that stores IPv6.
    """

    def set(self, value: str) -> None:
        """ Set current option value.

        :param str value: option value to set
        :return None: None
        """

        self.check('IPv6', Type.is_ipv6, value)
        self.value = value


class IPOption(Option):
    """ Subclass of hatsploit.lib.option module.

    This subclass of hatsploit.lib.option module is a representation
    of an option that stores IPv6/IPv4.
    """

    def set(self, value: str) -> None:
        """ Set current option value.

        :param str value: option value to set
        :return None: None
        """

        self.check('IP', Type().is_ip, value)
        self.value = value


class MACOption(Option):
    """ Subclass of hatsploit.lib.option module.

    This subclass of hatsploit.lib.option module is a representation
    of an option that stores MAC address.
    """

    def set(self, value: str) -> None:
        """ Set current option value.

        :param str value: option value to set
        :return None: None
        """

        self.check('MAC', Type.is_mac, value)
        self.value = value


class IPv4CIDROption(Option):
    """ Subclass of hatsploit.lib.option module.

    This subclass of hatsploit.lib.option module is a representation
    of an option that stores IPv4 CIDR.
    """

    def set(self, value: str) -> None:
        """ Set current option value.

        :param str value: option value to set
        :return None: None
        """

        self.check('IPv4 CIDR', Type().is_ipv4_cidr, value)
        self.value = value


class IPv6CIDROption(Option):
    """ Subclass of hatsploit.lib.option module.

    This subclass of hatsploit.lib.option module is a representation
    of an option that stores IPv6 CIDR.
    """

    def set(self, value: str) -> None:
        """ Set current option value.

        :param str value: option value to set
        :return None: None
        """

        self.check('IPv6 CIDR', Type().is_ipv6_cidr, value)
        self.value = value


class PortOption(Option):
    """ Subclass of hatsploit.lib.option module.

    This subclass of hatsploit.lib.option module is a representation
    of an option that stores TCP/UDP port.
    """

    def __init__(self, *args, **kwargs) -> None:
        """ Initialize port option.

        :return None: None
        """

        self.big = b''
        self.little = b''

        super().__init__(*args, **kwargs)

    def set(self, value: int) -> None:
        """ Set current option value.

        :param int value: option value to set
        :return None: None
        """

        self.check('port', Type().is_port, value)
        self.value = int(value)

        self.little = Socket().pack_port(self.value)
        self.big = Socket().pack_port(self.value, 'big')


class PortRangeOption(Option):
    """ Subclass of hatsploit.lib.option module.

    This subclass of hatsploit.lib.option module is a representation
    of an option that stores port range.
    """

    def set(self, value: str) -> None:
        """ Set current option value.

        :param str value: option value to set
        :return None: None
        """

        self.check('port range', Type().is_port_range, value)
        self.value = value


class NumberOption(Option):
    """ Subclass of hatsploit.lib.option module.

    This subclass of hatsploit.lib.option module is a representation
    of an option that stores float/integer.
    """

    def set(self, value: Union[int, float]) -> None:
        """ Set current option value.

        :param Union[int, float] value: option value to set
        :return None: None
        """

        self.check('number', Type().is_number, value)
        self.value = value


class IntegerOption(Option):
    """ Subclass of hatsploit.lib.option module.

    This subclass of hatsploit.lib.option module is a representation
    of an option that stores integer.
    """

    def set(self, value: int) -> None:
        """ Set current option value.

        :param int value: option value to set
        :return None: None
        """

        self.check('integer', Type.is_integer, value)
        self.value = int(value)


class FloatOption(Option):
    """ Subclass of hatsploit.lib.option module.

    This subclass of hatsploit.lib.option module is a representation
    of an option that stores float.
    """

    def set(self, value: float) -> None:
        """ Set current option value.

        :param float value: option value to set
        :return None: None
        """

        self.check('float', Type.is_float, value)
        self.value = float(value)


class BooleanOption(Option):
    """ Subclass of hatsploit.lib.option module.

    This subclass of hatsploit.lib.option module is a representation
    of an option that stores bool (yes/no).
    """

    def set(self, value: str) -> None:
        """ Set current option value.

        :param str value: option value to set
        :return None: None
        """

        self.check('boolean', Type.is_boolean, value)
        self.value = value.lower() in ['y', 'yes']
