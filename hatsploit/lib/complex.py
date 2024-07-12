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

from typing import Union

from hatsploit.lib.option import Option
from hatsploit.lib.modules import Modules
from hatsploit.lib.payloads import Payloads
from hatsploit.lib.encoders import Encoders
from hatsploit.lib.sessions import Sessions
from hatsploit.lib.mixins import PayloadMixin


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
        self.criteria = {}

        self.config = {
            'BadChars': b'',
            'Space': 2048
        }

        self.mixin = None

        self.modules = Modules()
        self.payloads = Payloads()
        self.encoders = Encoders()

    def run(self, method: str = 'run') -> bytes:
        """ Run current payload.

        :param str method: payload object method
        :return bytes: generated payload
        """

        if not self.payload:
            return b''

        return self.payloads.run_payload(
            self.payload, self.encoders.get_current_encoder(
                self.modules.get_current_module(), self.payload),
            method=method, badchars=self.config['BadChars'])

    def set(self, value: Union[str, int]) -> None:
        """ Set current option value.

        :param Union[str, int] value: option value to set
        :return None: None
        """

        value = self.modules.find_shorts('payload', value)
        module = self.modules.get_current_module()

        if not module:
            raise RuntimeError("No module specified for payload!")

        self.mixin = self.payloads.check_module_compatible(
            value, module)

        if not self.mixin:
            raise RuntimeError("Invalid option value, expected valid payload!")

        if self.mixin in self.criteria:
            self.config.update(self.criteria[self.mixin])
        self.payloads.add_payload(module, value)

        self.payload = self.payloads.get_module_payload(value, module)
        self.value = value


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
            platform = module.details['Platform']

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
