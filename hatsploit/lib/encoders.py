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

from typing import Union, Optional

from hatsploit.lib.encoder import Encoder
from hatsploit.lib.options import Options
from hatsploit.lib.module import Module
from hatsploit.lib.payload import Payload

from hatsploit.core.db.importer import Importer

from hatsploit.lib.storage import LocalStorage


class Encoders(object):
    """ Subclass of hatsploit.lib module.

    This subclass of hatsploit.lib module is intended for providing
    tools for working with HatSploit encoders.
    """

    def __init__(self) -> None:
        super().__init__()

        self.importer = Importer()
        self.options = Options()
        self.local_storage = LocalStorage()

    def encoders_completer(self, text: str) -> list:
        """ Tab-completion for encoders.

        :param str text: text to complete
        :return list: list of completions
        """

        encoders = self.get_encoders()
        matches = []

        if encoders:
            for database in encoders:
                for encoder in encoders[database]:
                    if encoder.startswith(text):
                        matches.append(encoder)

        return matches

    def get_encoders(self) -> dict:
        """ Get all encoders from local storage.

        :return dict: encoders, encoder names as keys and
        encoder objects as items
        """

        return self.local_storage.get("encoders", {})

    def get_imported_encoders(self) -> dict:
        """ Get all imported encoders from local storage.

        :return dict: encoders, encoder name as keys and
        encoder objects as items
        """

        return self.local_storage.get("imported_encoders", {})

    def get_database(self, encoder: str) -> str:
        """ Get database in which specific encoder exists.

        :param str encoder: encoder name
        :return str: database name
        """

        all_encoders = self.get_encoders()

        if all_encoders:
            for database in all_encoders:
                encoders = all_encoders[database]

                if encoder in encoders:
                    return database

        return ''

    def get_encoder(self, encoder: str) -> Union[Encoder, None]:
        """ Import and get imported encoder.

        :param str encoder: encoder name
        :return Union[Encoder, None]: imported encoder, None if failed to import
        """

        encoder_object = self.get_encoder_object(encoder)

        try:
            imported_encoder = self.importer.import_encoder(encoder_object['Path'])
            self.options.add_options(imported_encoder)
        except Exception:
            return None

        return imported_encoder

    def get_encoder_object(self, encoder: str) -> dict:
        """ Get encoder object, this object represents encoder details
        from the database.

        :param str encoder: encoder name
        :return dict: encoder object, encoder details
        """

        if self.check_exist(encoder):
            database = self.get_database(encoder)

            return self.get_encoders()[database][encoder]
        return {}

    def get_current_encoder(self, module: Module, payload: Payload) -> Union[Encoder, None]:
        """ Get current encoder, this is encoder which is currently
        used within current module and current payload.

        :param Module module: current module
        :param Payload payload: current payload
        :return Union[Encoder, None]: current encoder, None if no current encoder
        """

        imported_encoders = self.get_imported_encoders()

        if payload and module and imported_encoders and 'Encoder' in payload.details:
            module_name = module.details['Module']
            payload_name = payload.details['Payload']

            if module_name in imported_encoders and payload_name in imported_encoders[module_name]:
                name = payload.details['Encoder']['Value']

                return imported_encoders[module_name][payload_name].get(name, None)

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
                            encoder_object.details['Encoder']: encoder_object
                        })

                    else:
                        imported_encoders[module].update({
                            payload: {
                                encoder_object.details['Encoder']: encoder_object
                            }
                        })

                else:
                    imported_encoders.update({
                        module: {
                            payload: {
                                encoder_object.details['Encoder']: encoder_object
                            }
                        }
                    })

            else:
                imported_encoders = {
                    module: {
                        payload: {
                            encoder_object.details['Encoder']: encoder_object
                        }
                    }
                }

            self.local_storage.set("imported_encoders", imported_encoders)

        return encoder_object

    def check_exist(self, encoder: str) -> bool:
        """ Check if encoder exists in the database.

        :param str encoder: encoder name
        :return bool: True if exists else False
        """

        all_encoders = self.get_encoders()

        if all_encoders:
            for database in all_encoders:
                encoders = all_encoders[database]

                if encoder in encoders:
                    return True

        return False

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

    def check_payload_compatible(self, encoder: str, payload: Payload) -> bool:
        """ Check if encoder is compatible with the specific payload.

        :param str encoder: encoder name
        :param Payload payload: payload object
        :return bool: True if compatible else False
        """

        if self.check_exist(encoder):
            encoder = self.get_encoder_object(encoder)

            if encoder['Architecture'] == payload.details['Architecture']:
                return True

        return False

    def add_encoder(self, module: str, payload: str, encoder: str) -> None:
        """ Add encoder to module and payload which you want to reserve it for.

        :param str module: module which you want to reserve encoder for
        :param str payload: payload which you want to reserve encoder for
        :param str encoder: encoder name
        :return None: None
        :raises RuntimeError: with trailing error message
        """

        if not self.check_imported(module, payload, encoder):
            if not self.import_encoder(module, payload, encoder):
                raise RuntimeError(f"Failed to select encoder from database: {encoder}!")

    def set_option_value(self, encoder: Encoder, option: str, value: Optional[str] = None) -> bool:
        """ Set encoder option value.

        :param Encoder encoder: encoder object
        :param str option: option name
        :param Optional[str] value: option value
        :return bool: True if success else False
        """

        return self.options.set_option(encoder, option, value)

    @staticmethod
    def validate_options(encoder: Encoder) -> list:
        """ Validate missed encoder options.

        :param Encoder encoder: encoder object
        :return list: list of missed option names
        """

        missed = []

        if hasattr(encoder, "options"):
            for option in encoder.options:
                validate = encoder.options[option]

                if not validate['Value'] and validate['Value'] != 0 and validate['Required']:
                    missed.append(option)

        return missed
