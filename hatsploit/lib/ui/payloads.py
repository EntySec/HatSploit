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

import sys
import traceback

from hatasm import HatAsm

from typing import Union, Any, Optional

from pex.platform import Platform
from pex.arch import Arch

from hatsploit.core.db.db import DB

from hatsploit.lib.core.payload.const import SINGLE

from hatsploit.lib.core.payload import Payload
from hatsploit.lib.core.encoder import Encoder
from hatsploit.lib.core.module import Module

from hatsploit.lib.ui.encoders import Encoders

from hatsploit.lib.storage import STORAGE
from hatsploit.lib.mixins import PayloadMixin, PayloadGenericMixin


class Payloads(HatAsm):
    """ Subclass of hatsploit.lib module.

    This subclass of hatsploit.lib module is intended for providing
    tools for working with HatSploit payloads.
    """

    encoders = Encoders()

    def payloads_completer(self) -> list:
        """ Tab-completion for payloads.

        :return list: list of completions
        """

        return {payload: None for payload in self.get_payloads()}

    @staticmethod
    def get_payloads(criteria: dict = {}, query: dict = {}) -> dict:
        """ Get all payloads from local storage.

        :param dict criteria: DB search criteria
        :param dict query: payload search query
        :return dict: payloads, payload names as keys and
        payload objects as items
        """

        return DB(table='payloads').dump(
            criteria=criteria, query=query)

    @staticmethod
    def get_imported_payloads() -> dict:
        """ Get all imported payloads from local storage.

        :return dict: payloads, payload name as keys and
        payload objects as items
        """

        return STORAGE.get("imported_payloads")

    @staticmethod
    def get_payload(payload: str) -> Union[Payload, None]:
        """ Import and get imported payload.

        :param str payload: payload name
        :return Union[Payload, None]: imported payload, None if failed to import
        """

        try:
            payload_object = DB(table='payloads').load(
                criteria={'BaseName': payload}).get(payload)
            payload_object.update()

        except Exception:
            return

        return payload_object

    def get_payload_object(self, payload: str) -> dict:
        """ Get payload object, this object represents payload details
        from the database.

        :param str payload: payload name
        :return dict: payload object, payload details
        """

        return self.get_payloads(
            {'BaseName': payload}).get(payload, {})

    def get_current_payload(self, module: Module) -> Union[Payload, None]:
        """ Get current payload, this is payload which is currently
        used within current module.

        :param Module module: current module
        :return Union[Payload, None]: current payload, None if no current payload
        """

        if hasattr(module, 'payload'):
            return self.get_module_payload(module.payload.value, module)

    def get_module_payload(self, name: str, module: Module) -> Union[Payload, None]:
        """ Get payload imported within the module context.

        :param str name: payload name
        :param Module module: module object
        :return Union[Payload, None]: payload if exists
        """

        imported_payloads = self.get_imported_payloads()
        module_name = module.info['Module']

        if imported_payloads and module_name in imported_payloads:
            return imported_payloads[module_name].get(name, None)

    def search_payload(self, name: str) -> str:
        """ Get payload name by full payload name.

        Note: Payload name looks like this:
              - macos/x64/say
              Full payload name looks like this:
              - macOS x64 Say

        :param str name: payload name
        :return str: payload short name
        """

        payloads = self.get_payloads()

        for payload in payloads:
            if payloads[payload]['Name'].lower() == name.lower():
                return payload

        return ''

    def import_payload(self, module: str, payload: str) -> Union[Payload, None]:
        """ Import module.

        :param str module: name of module you want to reserve payload for
        :param str payload: payload name
        :return Union[Payload, None]: imported payload, None if failed to import
        """

        payload_object = self.get_payload(payload)

        if payload_object:
            imported_payloads = self.get_imported_payloads()

            if imported_payloads:
                if module in imported_payloads:
                    imported_payloads[module].update({
                        payload_object.info['Payload']: payload_object
                    })
                else:
                    imported_payloads.update({
                        module: {
                            payload_object.info['Payload']: payload_object
                        }
                    })
            else:
                imported_payloads = {
                    module: {
                        payload_object.info['Payload']: payload_object
                    }
                }

            STORAGE.set("imported_payloads", imported_payloads)

        return payload_object

    def check_exist(self, payload: str) -> bool:
        """ Check if payload exists in the database.

        :param str payload: payload name
        :return bool: True if exists else False
        """

        return payload in self.get_payloads()

    def check_usable(self, payload: str) -> bool:
        """ Check if payload is usable within the console.

        :param str payload: payload name
        :return bool: True if usable else False
        """

        payload = self.get_payload_object(payload)

        if payload and payload['Category'] == SINGLE:
            return True

        return False

    def check_imported(self, module: str, payload: str) -> bool:
        """ Check if payload is imported.

        :param str module: name of module which payload is reserved for
        :param str payload: payload name
        :return bool: True if imported else False
        """

        imported_payloads = self.get_imported_payloads()

        if imported_payloads:
            if module in imported_payloads:
                if payload in imported_payloads[module]:
                    return True

        return False

    def check_module_compatible(self, payload: str, module: Module) -> Union[PayloadMixin, None]:
        """ Check if payload is compatible with the specific module.

        :param str payload: payload name
        :param Module module: module object
        :return Union[PayloadMixin, None]: payload mixin if compatible else None
        """

        if not self.check_usable(payload):
            return

        if not module.payload.criteria:
            return PayloadGenericMixin

        payload = self.get_payload_object(payload)
        mixins = module.payload.criteria

        for mixin in mixins:
            types = mixins[mixin].get('Type', None)
            platforms = mixins[mixin].get('Platform', None)
            arches = mixins[mixin].get('Arch', None)

            if types and payload['Type'] not in types:
                continue

            if platforms and not any(payload['Platform'] == platform for platform in platforms):
                continue

            if arches and not any(payload['Arch'] == arch for arch in arches):
                continue

            return mixin

    def add_payload(self, module: Module, payload: str) -> None:
        """ Add payload to module which you want to reserve it for.

        :param str module: module object
        :param str payload: payload name
        :return None: None
        :raises RuntimeError: with trailing error message
        """

        module_name = module.info['Module']

        if not self.check_imported(module_name, payload):
            if not self.import_payload(module_name, payload):
                raise RuntimeError(f"Failed to select payload from database: {payload}!")

    def generate_payload(self, payload: str, options: dict = {},
                         encoder: Optional[str] = None,
                         *args, **kwargs) -> Any:
        """ Generate payload using specific payload and encoder.

        :param str payload: payload name
        :param dict options: dictionary, option names as keys and option values
        as items
        :param Optional[str] encoder: encoder name
        :return Any: payload returned by the specific payload
        """

        payload = self.get_payload(payload)

        if payload:
            for option in options:
                payload.set(option.lower(), options[option])

            if encoder:
                encoder = self.encoders.get_encoder(encoder)

                for option in options:
                    encoder.set(option.lower(), options[option])

            return self.run_payload(payload, encoder, *args, **kwargs)

    def pack_payload(self, payload: bytes, platform: Platform, arch: Arch, file_format: Optional[str] = None) -> bytes:
        """ Pack payload in the CPU executable.

        :param bytes payload: payload in bytes
        :param Platform platform: platform to pack executable for
        :param Arch arch: architecture to pack executable for
        :param Optional[str] file_format: file format to pack for
        :return bytes: CPU executable
        """

        return self.pack_exe(
            payload, arch, file_format if file_format else platform.exec)

    @staticmethod
    def detect_badchars(code: bytes, badchars: bytes) -> bool:
        """ Check if code contains badchars.

        :param bytes code: payload code
        :param bytes badchars: bad characters
        :return bool: True if code contains badchars else False
        """

        for char in badchars:
            if char in code:
                return True

        return False

    def fix_badchars(self, payload: Payload, code: bytes, badchars: bytes) -> bytes:
        """ Fix and remove bad characters from payload.

        :param Payload payload: payload object
        :param bytes code: payload code
        :param bytes badchars: bad characters
        :return bytes: fixed payload code
        """

        if not self.detect_badchars(code, badchars):
            return code

        all_encoders = self.encoders.get_encoders()

        if not all_encoders:
            return code

        for database in all_encoders:
            encoders = all_encoders[database]

            for encoder in encoders:
                if not self.encoders.check_payload_compatible(encoder, payload):
                    continue

                encoder = self.encoders.get_encoder(encoder)
                encoder.payload = code
                new_code = encoder.run()

                if not self.detect_badchars(new_code, badchars):
                    return new_code

    def run_payload(self, payload: Payload, encoder: Optional[Encoder] = None,
                    method: str = 'run', badchars: bytes = b'',
                    prepend: Union[bytes, str] = b'', append: Union[bytes, str] = b'') -> Any:
        """ Run payload and apply encoder to it.

        :param Payload payload: payload object
        :param Optional[Encoder] encoder: encoder object
        :param str method: payload generator method (run, stageN)
        :param bytes badchars: add custom bad chars to omit
        :param Union[bytes, str] prepend: prepend additional binary stub
        :param Union[bytes, str] append: append additional binary stub
        additional options
        :return Any: payload result
        """

        missed = payload.validate()

        if missed:
            raise RuntimeError(
                f"These options are failed to validate: {', '.join(missed)}!")

        if not hasattr(payload, method):
            raise RuntimeError(
                f"Payload does not have method: {method}!")

        code = prepend + getattr(payload, method)() + append

        if hasattr(payload, 'apply'):
            code = payload.apply(code)

        if not code:
            raise RuntimeError("Empty payload output detected!")

        if encoder:
            code = self.encoders.encode_payload(encoder, code)

        return self.fix_badchars(
            payload, code, payload.badchars.value + badchars)
