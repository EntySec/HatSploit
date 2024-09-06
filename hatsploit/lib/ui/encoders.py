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

from typing import Union

from hatsploit.lib.core.encoder import Encoder
from hatsploit.lib.core.module import Module
from hatsploit.lib.core.payload import Payload

from hatsploit.core.db.db import DB

from hatsploit.lib.storage import STORAGE


class Encoders(object):
    """ Subclass of hatsploit.lib module.

    This subclass of hatsploit.lib module is intended for providing
    tools for working with HatSploit encoders.
    """

    def encoders_completer(self) -> list:
        """ Tab-completion for encoders.

        :return list: list of completions
        """

        return {encoder: None for encoder in self.get_encoders()}

    @staticmethod
    def get_encoders(criteria: dict = {}, query: dict = {}) -> dict:
        """ Get all encoders from local storage.

        :param dict criteria: DB search criteria
        :param dict query: encoder search query
        :return dict: encoders, encoder names as keys and
        encoder objects as items
        """

        return DB(table='encoders').dump(
            criteria=criteria, query=query)

    @staticmethod
    def get_imported_encoders() -> dict:
        """ Get all imported encoders from local storage.

        :return dict: encoders, encoder name as keys and
        encoder objects as items
        """

        return STORAGE.get("imported_encoders", {})

    @staticmethod
    def get_encoder(encoder: str) -> Union[Encoder, None]:
        """ Import and get imported encoder.

        :param str encoder: encoder name
        :return Union[Encoder, None]: imported encoder, None if failed to import
        """

        try:
            encoder_object = DB(table='encoders').load(
                criteria={'BaseName': encoder}).get(encoder)
            encoder_object.update()

        except Exception:
            traceback.print_exc(file=sys.stdout)
            return

        return encoder_object

    def get_encoder_object(self, encoder: str) -> dict:
        """ Get encoder object, this object represents encoder details
        from the database.

        :param str encoder: encoder name
        :return dict: encoder object, encoder details
        """

        return self.get_encoders(
            {'BaseName': encoder}).get(encoder, {})

    def get_payload_encoder(self, name: str, module: Module, payload: Payload) -> Union[Encoder, None]:
        """ Get encoder associated with specific payload context.

        :param str name: encoder name
        :param Module module: module object
        :param Payload payload: payload object
        :return Union[Encoder, None]: encoder if exists
        """

        imported_encoders = self.get_imported_encoders()
        module_name = module.info['Module']
        payload_name = payload.info['Payload']

        if imported_encoders and module_name in imported_encoders \
                and payload_name in imported_encoders[module_name]:
            return imported_encoders[module_name][payload_name].get(name, None)

    def get_current_encoder(self, module: Module, payload: Payload) -> Union[Encoder, None]:
        """ Get current encoder, this is encoder which is currently
        used within current module and current payload.

        :param Module module: current module
        :param Payload payload: current payload
        :return Union[Encoder, None]: current encoder, None if no current encoder
        """

        if hasattr(payload, 'encoder'):
            return self.get_payload_encoder(payload.encoder.value, module, payload)

    def import_encoder(self, module: str, payload: str, encoder: str) -> Union[Encoder, None]:
        """ Import encoder.

        :param str module: module name which you want to reserve encoder for
        :param str payload: payload name which you want to reserve encoder for
        :param str encoder: encoder name
        :return Union[Encoder, None]: imported encoder, None if failed to import
        """

        encoder_object = self.get_encoder(encoder)

        if encoder_object:
            imported_encoders = self.get_imported_encoders()

            if imported_encoders:
                if module in imported_encoders:
                    if payload in imported_encoders[module]:
                        imported_encoders[module][payload].update({
                            encoder_object.info['Encoder']: encoder_object
                        })

                    else:
                        imported_encoders[module].update({
                            payload: {
                                encoder_object.info['Encoder']: encoder_object
                            }
                        })

                else:
                    imported_encoders.update({
                        module: {
                            payload: {
                                encoder_object.info['Encoder']: encoder_object
                            }
                        }
                    })

            else:
                imported_encoders = {
                    module: {
                        payload: {
                            encoder_object.info['Encoder']: encoder_object
                        }
                    }
                }

            STORAGE.set("imported_encoders", imported_encoders)

        return encoder_object

    def check_exist(self, encoder: str) -> bool:
        """ Check if encoder exists in the database.

        :param str encoder: encoder name
        :return bool: True if exists else False
        """

        return encoder in self.get_encoders()

    def check_imported(self, module: str, payload: str, encoder: str) -> bool:
        """ Check if encoder is imported.

        :param str module: module name which encoder is reserved for
        :param str payload: payload name which encoder is reserved for
        :param str encoder: encoder name
        :return bool: True if imported else False
        """

        imported_encoders = self.get_imported_encoders()

        if imported_encoders:
            if module in imported_encoders and payload in imported_encoder[module]:
                if encoder in imported_encoders[module][payload]:
                    return True

        return False

    @staticmethod
    def encode_payload(encoder: Encoder, code: bytes) -> bytes:
        """ Encode full payload or provided code.

        :param Encoder encoder: encoder object
        :param bytes code: payload code to encode
        :return bytes: encoded payload
        """

        missed = encoder.validate()

        if missed:
            raise RuntimeError(
                f"These options are failed to validate: {', '.join(missed)}!")

        for _ in range(encoder.iterations.value):
            encoder.payload = code
            code = encoder.run()

        return code

    def check_payload_compatible(self, encoder: str, payload: Payload) -> bool:
        """ Check if encoder is compatible with the specific payload.

        :param str encoder: encoder name
        :param Payload payload: payload object
        :return bool: True if compatible else False
        """

        if self.check_exist(encoder):
            encoder = self.get_encoder_object(encoder)

            if encoder['Arch'] == payload.info['Arch']:
                return True

        return False

    def add_encoder(self, module: Module, payload: Payload, encoder: str) -> None:
        """ Add encoder to module and payload which you want to reserve it for.

        :param Module module: module which you want to reserve encoder for
        :param Payload payload: payload which you want to reserve encoder for
        :param str encoder: encoder name
        :return None: None
        :raises RuntimeError: with trailing error message
        """

        module_name = module.info['Module']
        payload_name = payload.info['Payload']

        if not self.check_imported(module_name, payload_name, encoder):
            if not self.import_encoder(module_name, payload_name, encoder):
                raise RuntimeError(f"Failed to select encoder from database: {encoder}!")
