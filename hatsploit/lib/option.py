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

from pex.type import Type
from pex.socket import Socket

from hatsploit.lib.options import Option


class OptionResolver(Option):
    """ Subclass of hatsploit.lib module.

    This subclass of hatsploit.lib module is a wrapper for Option
    implementation which extends basic class allowing to call external
    methods like Modules, Payloads, Encoders or Sessions.
    """

    def __init__(self, *args, **kwargs):
        Option.__init__(self, *args, **kwargs)


class IPv4Option(OptionResolver):
    def set(self, value):
        self.check('IPv4', Type().types['ipv4'], value)
        self.value = value

        self.little = Socket().pack_host(self.value)
        self.big = Socket().pack_host(self.value, 'big')


class IPv6Option(OptionResolver):
    def set(self, value):
        self.check('IPv6', Type().types['ipv6'], value)
        self.value = value


class IPOption(OptionResolver):
    def set(self, value):
        self.check('IP', Type().types['ip'], value)
        self.value = value


class MACOption(OptionResolver):
    def set(self, value):
        self.check('MAC', Type().types['mac'], value)
        self.value = value


class IPv4CIDROption(OptionResolver):
    def set(self, value):
        self.check('IPv4 CIDR', Type().types['ipv4_cidr'], value)
        self.value = value


class IPv6CIDROption(OptionResolver):
    def set(self, value):
        self.check('IPv6 CIDR', Type().types['ipv6_cidr'], value)
        self.value = value


class PortOption(OptionResolver):
    def set(self, value):
        self.check('port', Type().types['port'], value)
        self.value = int(value)

        self.little = Socket().pack_port(self.value)
        self.big = Socket().pack_port(self.value, 'big')


class PortRangeOption(OptionResolver):
    def set(self, value):
        self.check('port range', Type().types['port_range'], value)
        self.value = value


class NumberOption(OptionResolver):
    def set(self, value):
        self.check('number', Type().types['number'], value)
        self.value = value


class IntegerOption(OptionResolver):
    def set(self, value):
        self.check('integer', Type().types['integer'], value)
        self.value = int(value)


class FloatOption(OptionResolver):
    def set(self, value):
        self.check('float', Type().types['float'], value)
        self.value = float(value)


class BooleanOption(OptionResolver):
    def set(self, value):
        self.check('boolean', Type().types['boolean'], value)

        if value.lower() in ['y', 'yes']:
            self.value = True
        else:
            self.value = False
