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

from typing import Union, Any

from pex.post.push import Push
from pex.post.method import select_method

from pex.platform import *

from hatsploit.lib.ui.option import (
    Option,
    IPv4Option,
    PortOption
)

from hatsploit.lib.core.payload.const import (
    ONE_SIDE,
    REVERSE_TCP
)

from hatsploit.lib.ui.modules import Modules
from hatsploit.lib.ui.payloads import Payloads
from hatsploit.lib.ui.encoders import Encoders
from hatsploit.lib.ui.sessions import Sessions

from hatsploit.lib.mixins import (
    PayloadMixin,
    PayloadDropMixin
)


class DropperOption(Option):
    """ Subclass of hatsploit.lib.option module.

    This subclass of hatsploit.lib.option module is a representation
    of an option that stores dropper.
    """

    def __init__(self, *args, **kwargs) -> None:
        """ Initialize payload option.

        :return None: None
        """

        self.modules = Modules()
        self.method = None

        self.srvhost = IPv4Option('SRVHOST', None, "HTTP server host.", True)
        self.srvport = PortOption('SRVPORT', 80, "HTTP server port.", True)
        self.urlpath = Option('URLPATH', "/", "File path on server", True)

        self.push = Push()

        super().__init__(*args, **kwargs)

    def set(self, value: str) -> None:
        """ Set current option value.

        :param str value: option value to set
        :return None: None
        """

        method = select_method(
            methods=self.push.methods,
            method=value
        )

        module = self.modules.get_current_module()

        if module:
            if hasattr(module, 'payload') and module.payload.payload:
                method = select_method(
                    methods=self.push.methods,
                    platform=module.payload.info['Platform'],
                    method=value
                )

                if not method:
                    raise RuntimeError("Invalid option value, expected valid dropper!")

                if method.name != value and value != 'auto':
                    raise RuntimeError("Invalid option value, expected valid dropper!")

            if value in ['wget', 'curl']:
                module.srvhost = self.srvhost
                module.srvport = self.srvport
                module.urlpath = self.urlpath

                self.srvport.visible = True
                self.srvhost.visible = True
                self.urlpath.visible = True
            else:
                self.srvport.visible = False
                self.srvhost.visible = False
                self.urlpath.visible = False

        self.method = method
        self.value = value


class PayloadOption(Option):
    """ Subclass of hatsploit.lib.option module.

    This subclass of hatsploit.lib.option module is a representation
    of an option that stores payload object.
    """

    def __init__(self, *args, **kwargs) -> None:
        """ Initialize payload option.

        :return None: None
        """

        super().__init__(*args, **kwargs)

        self.payload = None
        self.stage = None

        self.info = {}
        self.criteria = {}

        self.config = {
            'BadChars': b'',
            'Space': 2048,
            'Append': b'',
            'Prepend': b''
        }

        self.mixin = None

        self.modules = Modules()
        self.payloads = Payloads()
        self.encoders = Encoders()

    def run(self, method: str = 'run', stage: bool = False) -> Union[Any, None]:
        """ Run current payload.

        :param str method: payload object method
        :param bool stage: run stage instead of payload
        :return Union[Any, None]: generated payload or None
        """

        payload = self.payload

        if stage:
            payload = self.stage

        if not payload:
            return b''

        if stage:
            for option in self.payload.options:
                payload.set(option, self.payload.options[option].value)

        buffer = self.payloads.run_payload(
            payload, self.encoders.get_current_encoder(
                self.modules.get_current_module(), payload),
            method=method,
            badchars=self.config['BadChars'],
            prepend=self.config['Prepend'],
            append=self.config['Append']
        )

        return buffer

    def set(self, value: Union[str, int]) -> None:
        """ Set current option value.

        :param Union[str, int] value: option value to set
        :return None: None
        """

        value = self.modules.find_shorts('payload', value)
        module = self.modules.get_current_module()

        if not module:
            raise RuntimeError("No module specified for payload!")

        if not self.payloads.check_usable(value):
            raise RuntimeError("Invalid option value, expected valid payload!")

        self.mixin = self.payloads.check_module_compatible(
            value, module)

        if not self.mixin:
            raise RuntimeError("Invalid option value, expected valid payload!")

        if self.mixin in self.criteria:
            self.config.update(self.criteria[self.mixin])
        self.payloads.add_payload(module, value)

        self.payload = self.payloads.get_module_payload(value, module)
        self.info.update(self.payload.info)
        self.value = value

        stage = self.payload.info['Stage']

        if not stage:
            stage = '/'.join((str(self.info['Platform']),
                              str(self.info['Arch']),
                              self.info['Type'] if self.info['Type'] != ONE_SIDE
                              else REVERSE_TCP))

        if not self.payloads.check_exist(stage):
            return

        self.payloads.add_payload(module, stage)
        self.stage = self.payloads.get_module_payload(stage, module)


class EncoderOption(Option):
    """ Subclass of hatsploit.lib.option module.

    This subclass of hatsploit.lib.option module is a representation
    of an option that stores encoder object.
    """

    def __init__(self, *args, **kwargs) -> None:
        """ Initialize encoder option.

        :return None: None
        """

        super().__init__(*args, **kwargs)

        self.encoder = None

        self.modules = Modules()
        self.payloads = Payloads()
        self.encoders = Encoders()

    def set(self, value: Union[str, int]) -> None:
        """ Set current option value.

        :param Union[str, int] value: option value to set
        :return None: None
        """

        value = self.modules.find_shorts('encoder', value)
        module = self.modules.get_current_module()
        payload = self.payloads.get_current_payload(module)

        if module and payload:
            if self.encoders.check_payload_compatible(value, payload):
                self.encoders.add_encoder(module, payload, value)
                self.encoder = self.encoders.get_payload_encoder(
                    value, module, payload)
                self.value = value

                return

        raise RuntimeError("Invalid option value, expected valid encoder!")


class SessionOption(Option):
    """ Subclass of hatsploit.lib.option module.

    This subclass of hatsploit.lib.option module is a representation
    of an option that stores session object.
    """

    def __init__(self, *args, platforms: list = [], type: str = '', **kwargs):
        """ Initialize session option.

        :param list platforms: supported platforms
        :param str type: type of session
        :return None: None
        """

        Option.__init__(self, *args, **kwargs)

        self.sessions = Sessions()
        self.modules = Modules()

        self.platforms = platforms
        self.type = type

        self.session = None

    def set(self, value: int) -> None:
        """ Set current option value.

        :param int value: option value to set
        :return None: None
        """

        value = int(value)
        module = self.modules.get_current_module()

        if module:
            platform = module.info['Platform']

            if not self.platforms:
                if not self.sessions.check_exist(value, platform, self.type):
                    raise RuntimeError("Invalid value, expected valid session!")
            else:
                session = 0

                for platform in self.platforms:
                    if self.sessions.check_exist(value, platform, self.type):
                        session = 1
                        break

                if not session:
                    raise RuntimeError("Invalid value, expected valid session!")
        else:
            raise RuntimeError("Invalid value, expected valid session!")

        self.value = value
        self.session = self.sessions.get_session(value)
