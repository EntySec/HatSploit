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

from hatvenom import HatVenom
from pex.type import Type

from typing import Union, Any, Optional

from pex.platform.types import Platform
from pex.arch.types import Arch

from hatsploit.core.db.importer import Importer

from hatsploit.lib.payload import Payload
from hatsploit.lib.options import Options
from hatsploit.lib.encoder import Encoder
from hatsploit.lib.module import Module
from hatsploit.lib.encoders import Encoders
from hatsploit.lib.storage import LocalStorage


class Payloads(object):
    """ Subclass of hatsploit.lib module.

    This subclass of hatsploit.lib module is intended for providing
    tools for working with HatSploit payloads.
    """

    def __init__(self) -> None:
        super().__init__()

        self.hatvenom = HatVenom()

        self.types = Type()

        self.importer = Importer()
        self.options = Options()
        self.local_storage = LocalStorage()
        self.encoders = Encoders()

    def payloads_completer(self, text: str) -> list:
        """ Tab-completion for payloads.

        :param str text: text to complete
        :return list: list of completions
        """

        payloads = self.get_payloads()
        matches = []

        if payloads:
            for database in payloads:
                for payload in payloads[database]:
                    if payload.startswith(text):
                        matches.append(payload)

        return matches

    def get_payloads(self) -> dict:
        """ Get all payloads from local storage.

        :return dict: payloads, payload names as keys and
        payload objects as items
        """

        return self.local_storage.get("payloads")

    def get_imported_payloads(self) -> dict:
        """ Get all imported payloads from local storage.

        :return dict: payloads, payload name as keys and
        payload objects as items
        """

        return self.local_storage.get("imported_payloads")

    def get_database(self, payload: str) -> str:
        """ Get database in which specific payload exists.

        :param str payload: payload name
        :return str: database name
        """

        all_payloads = self.get_payloads()

        if all_payloads:
            for database in all_payloads:
                payloads = all_payloads[database]

                if payload in payloads:
                    return database

        return ''

    def get_payload(self, payload: str) -> Union[Payload, None]:
        """ Import and get imported payload.

        :param str payload: payload name
        :return Union[Payload, None]: imported payload, None if failed to import
        """

        payload_object = self.get_payload_object(payload)

        try:
            imported_payload = self.importer.import_payload(payload_object['Path'])
            self.options.add_options(imported_payload)
        except Exception:
            return None

        return imported_payload

    def get_payload_object(self, payload: str) -> dict:
        """ Get payload object, this object represents payload details
        from the database.

        :param str payload: payload name
        :return dict: payload object, payload details
        """

        if self.check_exist(payload):
            database = self.get_database(payload)

            return self.get_payloads()[database][payload]
        return {}

    def get_current_payload(self, module: Module) -> Union[Payload, None]:
        """ Get current encoder, this is encoder which is currently
        used within current module.

        :param Module module: current module
        :return Union[Payload, None]: current payload, None if no current payload
        """

        imported_payloads = self.get_imported_payloads()

        if module and imported_payloads and 'Payload' in module.details:
            module_name = module.details['Module']

            if module_name in imported_payloads:
                name = module.details['Payload']['Value']

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

        for database in payloads:
            for payload in payloads[database]:
                if payloads[database][payload]['Name'].lower() == name.lower():
                    return payloads[database][payload]['Payload']

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
                        payload_object.details['Payload']: payload_object
                    })
                else:
                    imported_payloads.update({
                        module: {
                            payload_object.details['Payload']: payload_object
                        }
                    })
            else:
                imported_payloads = {
                    module: {
                        payload_object.details['Payload']: payload_object
                    }
                }

            self.local_storage.set("imported_payloads", imported_payloads)

        return payload_object

    def check_exist(self, payload: str) -> bool:
        """ Check if payload exists in the database.

        :param str payload: payload name
        :return bool: True if exists else False
        """

        all_payloads = self.get_payloads()

        if all_payloads:
            for database in all_payloads:
                payloads = all_payloads[database]

                if payload in payloads:
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

    def check_module_compatible(self, payload: str, module: Module) -> bool:
        """ Check if payload is compatible with the specific module.

        :param str payload: payload name
        :param Module module: module object
        :return bool: True if compatible else False
        """

        payload = self.get_payload_object(payload)

        if payload:
            if 'Payload' in module.details:
                types = module.details['Payload'].get('Types', None)
                platforms = module.details['Payload'].get('Platforms', None)
                arches = module.details['Payload'].get('Arches', None)

                if types and payload['Type'] not in types:
                    return False

                if platforms and not any(payload['Platform'] == platform for platform in platforms):
                    return False

                if arches and not any(payload['Arch'] == arch for arch in arches):
                    return False

            return True

        return False

    def add_payload(self, module: str, payload: str) -> None:
        """ Add payload to module which you want to reserve it for.

        :param str module: module which you want to reserve encoder for
        :param str payload: payload name
        :return None: None
        :raises RuntimeError: with trailing error message
        """

        if not self.check_imported(module, payload):
            if not self.import_payload(module, payload):
                raise RuntimeError(f"Failed to select payload from database: {payload}!")

    def generate_payload(self, payload: str, options: dict = {}, encoder: Optional[str] = None,
                         implant: bool = False) -> Any:
        """ Generate payload using specific payload and encoder.

        :param str payload: payload name
        :param dict options: dictionary, option names as keys and option values
        as items
        :param Optional[str] encoder: encoder name
        :param bool implant: True to output implant else False
        :return Any: payload returned by the specific payload
        """

        payload = self.get_payload(payload)

        if payload:
            for option in options:
                payload.set(option, options[option])

            if encoder:
                encoder = self.encoders.get_encoder(encoder)

                for option in options:
                    encoder.set(option, options[option])

            return self.run_payload(payload, encoder, implant)

    def pack_payload(self, payload: bytes, platform: Platform, arch: Arch, file_format: Optional[str] = None) -> bytes:
        """ Pack payload in the CPU executable.

        :param bytes payload: payload in bytes
        :param Platform platform: platform to pack executable for
        :param Arch arch: architecture to pack executable for
        :param Optional[str] file_format: file format to pack for
        :return bytes: CPU executable
        """

        return self.hatvenom.generate(
            platform.exec if not file_format else file_format, str(arch), payload)

    @staticmethod
    def detect_badchars(code: bytes, badchars: bytes) -> bool:
        """ Check if code contains badchars.

        :param bytes code: payload code
        :param bytes badchars: bad characters
        :return bool: True if code contains badchars else False
        """

        if badchars:
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

        if all_encoders:
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

        return code

    def run_payload(self, payload: Payload, encoder: Optional[Encoder] = None, implant: bool = False) -> Any:
        """ Run payload and apply encoder to it.

        :param Payload payload: payload object
        :param Optional[Encoder] encoder: encoder object
        :param bool implant: True to output implant else False
        :return Any: payload result
        """

        if not self.validate_options(payload):
            code = payload.run()

            if implant:
                if hasattr(payload, "implant"):
                    code = payload.implant()

            if not code:
                raise RuntimeError("Payload does not support generation!")

            if encoder:
                for _ in range(encoder.iterations.value):
                    encoder.payload = code
                    code = encoder.run()

            return self.fix_badchars(
                payload, code, payload.badchars.value)

    @staticmethod
    def validate_options(payload: Payload) -> list:
        """ Validate missed payload options.

        :param Payload payload: payload object
        :return list: list of missed option names
        """

        missed = []

        if hasattr(payload, "options"):
            for option in payload.options:
                validate = payload.options[option]

                if validate['Value'] is None and validate['Required']:
                    missed.append(option)

        return missed
