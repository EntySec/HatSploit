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

from hatsploit.lib.option import OptionResolver

from hatsploit.lib.modules import Modules
from hatsploit.lib.payloads import Payloads
from hatsploit.lib.encoders import Encoders
from hatsploit.lib.sessions import Sessions


class PayloadOption(OptionResolver):
    modules = Modules()
    payloads = Payloads()

    def set(self, value):
        value = self.modules.find_shorts('payload', value)
        module = self.modules.get_current_module()

        if module:
            if self.payloads.check_module_compatible(value, module):
                module_name = module.details['Module']

                self.payloads.add_payload(module_name, value)

                if 'Payload' not in module.details:
                    module.details['Payload'] = {}

                module.details['Payload']['Value'] = value

                self.payload = self.payloads.get_current_payload(module)
                self.value = value

                return

        raise RuntimeError("Invalid option value, expected valid payload!")


class EncoderOption(OptionResolver):
    modules = Modules()
    payloads = Payloads()
    encoders = Encoders()

    def set(self, value):
        value = self.modules.find_shorts('encoder', value)
        module = self.modules.get_current_module()
        payload = self.payloads.get_current_payload(module)

        if module and payload:
            if self.encoders.check_payload_compatible(value, payload):
                module_name = module.details['Module']
                payload_name = payload.details['Payload']

                self.encoders.add_encoder(module_name, payload_name, value)

                if 'Encoder' not in payload.details:
                    payload.details['Encoder'] = {}

                payload.details['Encoder']['Value'] = value

                self.encoder = self.encoders.get_current_encoder(module, payload)
                self.value = value

                return

        raise RuntimeError("Invalid option value, expected valid encoder!")


class SessionOption(OptionResolver):
    def __init__(self, *args, platforms: list = [], type: str = '', **kwargs):
        super(OptionResolver, self).__init__(*args, **kwargs)

        self.sessions = Sessions()
        self.modules = Modules()

        self.platforms = platforms
        self.type = type

    def set(self, value):
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
                    if self.sessions.check_exist(value, platform.strip(), self.type):
                        session = 1
                        break

                if not session:
                    raise RuntimeError("Invalid value, expected valid session!")
        else:
            raise RuntimeError("Invalid value, expected valid session!")

        self.value = value
        self.session = self.sessions.get_session(value)
