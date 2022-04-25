#!/usr/bin/env python3

#
# MIT License
#
# Copyright (c) 2020-2022 EntySec
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

from hatsploit.core.db.importer import Importer
from hatsploit.core.cli.badges import Badges

from hatsploit.lib.storage import LocalStorage


class Encoders:
    importer = Importer()
    badges = Badges()

    local_storage = LocalStorage()

    def encoders_completer(self, text):
        encoders = self.get_encoders()
        matches = []

        if encoders:
            for database in encoders:
                for encoder in encoders[database]:
                    if encoder.startswith(text):
                        matches.append(encoder)

        return matches

    def get_encoders(self):
        return self.local_storage.get("encoders")

    def get_imported_encoders(self):
        return self.local_storage.get("imported_encoders")

    def get_database(self, name):
        all_encoders = self.get_encoders()
        if all_encoders:
            for database in all_encoders:
                encoders = all_encoders[database]

                if name in encoders:
                    return database
        return None

    def get_encoder(self, encoder):
        encoder_object = self.get_encoder_object(encoder)
        try:
            imported_encoder = self.importer.import_encoder(encoder_object['Path'])
        except Exception:
            return None
        return imported_encoder

    def get_encoder_object(self, encoder):
        if self.check_exist(encoder):
            database = self.get_database(encoder)
            return self.get_encoders()[database][encoder]
        return None

    def get_current_encoder(self):
        imported_encoders = self.get_imported_encoders()

        current_payload = self.get_current_payload()
        current_module = self.get_current_module()

        if current_payload and current_module and imported_encoders:
            current_module_name = current_module.details['Module']
            current_payload_name = current_payload.details['Payload']

            if current_module_name in imported_encoders:
                if current_payload_name in imported_encoders[current_module_name]:
                    if hasattr(current_module, "options") and 'ENCODER' in current_module.options:
                        name = current_module.options['ENCODER']['Value']
                        return imported_encoders[current_module_name][current_payload_name][name]
        return None

    def get_current_module(self):
        if self.local_storage.get("current_module"):
            return self.local_storage.get_array(
                "current_module",
                self.local_storage.get("current_module_number")
            )
        return None

    def get_current_payload(self):
        imported_payloads = self.local_storage.get("imported_payloads")
        current_module_object = self.get_current_module()

        if current_module_object:
            current_module_name = current_module_object.details['Module']

            if hasattr(current_module_object, "payload"):
                name = current_module_object.payload['Value']

                if imported_payloads:
                    if current_module_name in imported_payloads:
                        if name in imported_payloads[current_module_name]:
                            return imported_payloads[current_module_name][name]
        return None

    def import_encoder(self, module_name, payload_name, encoder):
        encoder_object = self.get_encoder(encoder)

        if encoder_object:
            current_payload_name = payload_name
            current_module_name = module_name

            imported_encoders = self.get_imported_encoders()
            if imported_encoders:
                if current_module_name in imported_encoders:
                    if current_payload_name in imported_encoders[current_module_name]:
                        imported_encoders[current_module_name][current_payload_name].update({
                            encoder_object.details['Encoder']: encoder_object
                        })
                    else:
                        imported_encoders[current_module_name].update({
                            current_payload_name: {
                                encoder_object.details['Encoder']: encoder_object
                            }
                        })
                else:
                    imported_encoders.update({
                        current_module_name: {
                            current_payload_name: {
                                encoder_object.details['Encoder']: encoder_object
                            }
                        }
                    })
            else:
                imported_encoders = {
                    current_module_name: {
                        current_payload_name: {
                            encoder_object.details['Encoder']: encoder_object
                        }
                    }
                }

            self.local_storage.set("imported_encoders", imported_encoders)

        return encoder_object

    def check_exist(self, encoder):
        all_encoders = self.get_encoders()
        if all_encoders:
            for database in all_encoders:
                encoders = all_encoders[database]

                if encoder in encoders:
                    return True
        return False

    def check_imported(self, module_name, payload_name, encoder):
        imported_encoders = self.get_imported_encoders()

        current_payload_name = payload_name
        current_module_name = module_name

        if imported_encoders:
            if current_module_name in imported_encoders:
                if current_payload_name in imported_encoders[current_module_name]:
                    if encoder in imported_encoders[current_module_name][current_payload_name]:
                        return True
        return False

    def check_payload_compatible(self, value, architecture):
        if self.check_exist(value):
            encoder = self.get_encoder_object(value)

            if encoder['Architecture'] == architecture:
                return True
        return False

    def add_encoder(self, module_name, payload_name, encoder):
        if not self.check_imported(module_name, payload_name, encoder):
            encoder_object = self.import_encoder(module_name, payload_name, encoder)
            if not encoder_object:
                self.badges.print_error("Failed to select encoder from database!")
                return False
        return True
