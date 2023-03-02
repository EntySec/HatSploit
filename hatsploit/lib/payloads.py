"""
MIT License

Copyright (c) 2020-2022 EntySec

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

from hatsploit.core.db.importer import Importer
from hatsploit.lib.encoders import Encoders
from hatsploit.lib.options import Options
from hatsploit.lib.storage import LocalStorage


class Payloads:
    hatvenom = HatVenom()

    types = Type()

    importer = Importer()
    options = Options()
    local_storage = LocalStorage()
    encoders = Encoders()

    def payloads_completer(self, text):
        payloads = self.get_payloads()
        matches = []

        if payloads:
            for database in payloads:
                for payload in payloads[database]:
                    if payload.startswith(text):
                        matches.append(payload)

        return matches

    def get_payloads(self):
        return self.local_storage.get("payloads")

    def get_imported_payloads(self):
        return self.local_storage.get("imported_payloads")

    def get_database(self, name):
        all_payloads = self.get_payloads()
        if all_payloads:
            for database in all_payloads:
                payloads = all_payloads[database]

                if name in payloads:
                    return database
        return None

    def get_payload(self, payload):
        payload_object = self.get_payload_object(payload)
        try:
            imported_payload = self.importer.import_payload(payload_object['Path'])
        except Exception:
            return None
        return imported_payload

    def get_payload_object(self, payload):
        if self.check_exist(payload):
            database = self.get_database(payload)
            return self.get_payloads()[database][payload]
        return None

    def get_current_payload(self, current_module):
        imported_payloads = self.get_imported_payloads()
        current_module_object = current_module

        if current_module_object:
            current_module_name = current_module_object.details['Module']

            if hasattr(current_module_object, "payload"):
                name = current_module_object.payload['Value']

                if imported_payloads:
                    if current_module_name in imported_payloads:
                        if name in imported_payloads[current_module_name]:
                            return imported_payloads[current_module_name][name]
        return None

    def search_payload(self, name):
        payloads = self.get_payloads()

        for database in payloads:
            for payload in payloads[database]:
                if payloads[database][payload]['Name'].lower() == name.lower():
                    return payloads[database][payload]['Payload']
        return None

    def import_payload(self, module_name, payload):
        payload_object = self.get_payload(payload)

        if payload_object:
            current_module_name = module_name

            imported_payloads = self.get_imported_payloads()
            if imported_payloads:
                if current_module_name in imported_payloads:
                    imported_payloads[current_module_name].update({
                        payload_object.details['Payload']: payload_object
                    })
                else:
                    imported_payloads.update({
                        current_module_name: {
                            payload_object.details['Payload']: payload_object
                        }
                    })
            else:
                imported_payloads = {
                    current_module_name: {
                        payload_object.details['Payload']: payload_object
                    }
                }
            self.local_storage.set("imported_payloads", imported_payloads)

        return payload_object

    def check_exist(self, payload):
        all_payloads = self.get_payloads()
        if all_payloads:
            for database in all_payloads:
                payloads = all_payloads[database]

                if payload in payloads:
                    return True
        return False

    def check_imported(self, module_name, payload):
        imported_payloads = self.get_imported_payloads()
        current_module_name = module_name

        if imported_payloads:
            if current_module_name in imported_payloads:
                if payload in imported_payloads[current_module_name]:
                    return True
        return False

    def check_module_compatible(self, value, types, platforms, architectures):
        if self.check_exist(value):
            payload = self.get_payload_object(value)

            if types:
                if payload['Type'] not in types:
                    return False

            if platforms:
                if payload['Platform'] not in platforms:
                    return False

            if architectures:
                if payload['Architecture'] not in architectures:
                    return False

            return True
        return False

    def add_payload(self, module_name, payload):
        if not self.check_imported(module_name, payload):
            payload_object = self.import_payload(module_name, payload)
            if not payload_object:
                raise RuntimeError(f"Failed to select payload from database: {payload}!")

    def generate_payload(self, payload, options={}, encoder=None):
        payload_object = self.get_payload(payload)
        if payload_object:
            self.options.add_payload_handler(payload_object)

            if hasattr(payload_object, "options"):
                for option in options:
                    payload_object.options[option]['Value'] = options[option]

            encoder_object = None
            if encoder:
                encoder_object = self.encoders.get_encoder(encoder)

            return self.run_payload(payload_object, encoder_object)
        return None

    def pack_payload(self, payload, platform, architecture):
        formats = self.types.formats
        architectures = self.types.architectures

        exec_f = None

        if architecture in architectures['cpu']:
            for fmt in formats:
                if platform in formats[fmt]:
                    exec_f = fmt

            return self.hatvenom.generate(exec_f, architecture, payload)
        return payload

    def run_payload(self, payload_object, encoder_object):
        if not self.validate_options(payload_object):
            payload = payload_object.run()

            if encoder_object:
                encoder_object.payload = payload
                payload = encoder_object.run()

            return payload

        return None

    @staticmethod
    def validate_options(payload_object):
        current_payload = payload_object
        missed = ""

        if hasattr(current_payload, "options"):
            for option in current_payload.options:
                current_option = current_payload.options[option]
                if not current_option['Value'] and current_option['Value'] != 0 and current_option['Required']:
                    missed += option + ', '

        return missed
