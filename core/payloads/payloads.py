#!/usr/bin/env python3

#
# MIT License
#
# Copyright (c) 2020-2021 EntySec
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

import os

from core.db.importer import importer
from core.base.storage import local_storage
from core.cli.badges import badges

class payloads:
    def __init__(self):
        self.importer = importer()
        self.local_storage = local_storage()
        self.badges = badges()

    def check_exist(self, name):
        if self.check_style(name):
            all_payloads = self.local_storage.get("payloads")
            if all_payloads:
                for database in all_payloads.keys():
                    payloads = all_payloads[database]

                    platform = self.get_platform(name)
                    architecture = self.get_architecture(name)

                    if platform in payloads.keys():
                        if architecture in payloads[platform].keys():
                            payload = self.get_name(name)
                            if payload in payloads[platform][architecture].keys():
                                return True
        return False

    def check_style(self, name):
        if len(name.split('/')) >= 3:
            return True
        return False

    def get_platform(self, name):
        if self.check_style(name):
            return name.split('/')[0]
        return None

    def get_architecture(self, name):
        if self.check_style(name):
            return name.split('/')[1]
        return None

    def get_name(self, name):
        if self.check_style(name):
            return os.path.join(*(name.split(os.path.sep)[2:]))
        return None

    def get_payload_object(self, platform, architecture, name):
        payload_full_name = self.get_full_name(platform, architecture, name)
        if self.check_exist(payload_full_name):
            database = self.get_database(payload_full_name)
            return self.local_storage.get("payloads")[database][platform][architecture][name]
        return None

    def get_database(self, name):
        if self.check_style(name):
            all_payloads = self.local_storage.get("payloads")
            if all_payloads:
                for database in all_payloads.keys():
                    payloads = all_payloads[database]

                    platform = self.get_platform(name)
                    architecture = self.get_architecture(name)

                    if platform in payloads.keys():
                        if architecture in payloads[platform].keys():
                            payload = self.get_name(name)
                            if payload in payloads[platform][architecture].keys():
                                return database
        return None

    def get_full_name(self, platform, architecture, name):
        return platform + '/' + architecture + '/' + name

    def check_current_module(self):
        if self.local_storage.get("current_module"):
            if len(self.local_storage.get("current_module")) > 0:
                return True
        return False
    
    def get_current_module_object(self):
        if self.check_current_module():
            return self.local_storage.get_array("current_module", self.local_storage.get("current_module_number"))
        return None
    
    def get_current_module_name(self):
        if self.check_current_module():
            return self.local_storage.get_array("current_module", self.local_storage.get("current_module_number")).details['Module']
        return None
    
    def import_payload(self, platform, architecture, name):
        payloads = self.get_payload_object(platform, architecture, name)
        try:
            payload_object = self.importer.import_payload(payloads['Path'])
            current_module_name = self.get_current_module_name()

            imported_payloads = self.local_storage.get("imported_payloads")
            if imported_payloads:
                if current_module_name in imported_payloads.keys():
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
        except Exception:
            return None
        return payload_object
        
    def check_imported(self, name):
        imported_payloads = self.local_storage.get("imported_payloads")
        current_module_name = self.get_current_module_name()
        
        if imported_payloads:
            if current_module_name in imported_payloads.keys():
                if name in imported_payloads[current_module_name].keys():
                    return True
        return False
    
    def get_current_payload(self):
        imported_payloads = self.local_storage.get("imported_payloads")
        current_module_object = self.get_current_module_object()
        current_module_name = current_module_object.details['Module']

        if hasattr(current_module_object, "options"):
            for option in current_module_object.options.keys():
                if current_module_object.options[option]['Type'].lower() == 'payload':
                    name = current_module_object.options[option]['Value']
                    if current_module_name in imported_payloads.keys():
                        if name in imported_payloads[current_module_name].keys():
                            return imported_payloads[current_module_name][name]
        return None
        
    def add_payload(self, platform, architecture, name):
        payloads = self.get_payload_object(platform, architecture, name)

        not_installed = list()
        for dependence in payloads['Dependencies']:
            if not self.importer.import_check(dependence):
                not_installed.append(dependence)
        if not not_installed:
            imported_payloads = self.local_storage.get("imported_payloads")
            full_name = self.get_full_name(platform, architecture, name)

            if not self.check_imported(full_name):
                payload_object = self.import_payload(platform, architecture, name)
                if not payload_object:
                    self.badges.output_error("Failed to select payload from database!")
                    return False
        else:
            self.badges.output_error("Payload depends this dependencies which is not installed:")
            for dependence in not_installed:
                self.badges.output_empty("    * " + dependence)
            return False
        return True
