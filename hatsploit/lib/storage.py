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

import json


class GlobalStorage:
    def __init__(self, file):
        self.file = file

    def set_all(self):
        storage_variables = json.load(open(self.file))
        for variable in storage_variables:
            if storage_variables[variable] == "True":
                variable_value = True
            elif storage_variables[variable] == "False":
                variable_value = False
            elif storage_variables[variable] == "None":
                variable_value = None
            else:
                variable_value = storage_variables[variable]
            LocalStorage.set(variable, variable_value)

    def get_all(self):
        storage_variables = json.load(open(self.file))
        return storage_variables

    def set(self, variable, value):
        storage_variables = json.load(open(self.file))
        old_storage = storage_variables
        new_storage = open(self.file, 'w')

        old_storage[variable] = str(value)
        new_storage.write(str(old_storage).replace("'", '"'))
        new_storage.close()

    def get(self, variable):
        storage_variables = json.load(open(self.file))
        if variable in storage_variables:
            return storage_variables[variable]
        return None

    def delete(self, variable):
        storage_variables = json.load(open(self.file))
        old_storage = storage_variables

        if variable in old_storage:
            new_storage = open(self.file, 'w')

            del old_storage[variable]
            new_storage.write(str(old_storage).replace("'", '"'))
            new_storage.close()
        else:
            pass


class LocalStorage:
    @staticmethod
    def get_all():
        return globals()

    @staticmethod
    def add(name):
        globals()[name] = None

    @staticmethod
    def set(name, value):
        globals()[name] = value

    @staticmethod
    def update(name, value):
        try:
            globals()[name].update(value)
        except Exception:
            pass

    @staticmethod
    def add_array(name, value):
        try:
            globals()[name].append(value)
        except Exception:
            pass

    @staticmethod
    def get_array(name, value):
        try:
            return globals()[name][value]
        except Exception:
            return None

    @staticmethod
    def set_array(name, value1, value2):
        try:
            globals()[name][value1] = value2
        except Exception:
            pass

    @staticmethod
    def delete_element(name, value):
        try:
            del globals()[name][value]
        except Exception:
            pass

    @staticmethod
    def delete(name):
        try:
            del globals()[name]
        except Exception:
            pass

    @staticmethod
    def get(name):
        try:
            return globals()[name]
        except Exception:
            return None

    @staticmethod
    def set_module_option(name, number, option, value):
        try:
            globals()[name][number].options[option]['Value'] = value
        except Exception:
            pass

    @staticmethod
    def set_module_payload(name, number, value):
        try:
            globals()[name][number].payload['Value'] = value
        except Exception:
            pass

    @staticmethod
    def set_payload_option(module_name, payload_name, option, value):
        try:
            globals()["imported_payloads"][module_name][payload_name].options[option]['Value'] = value
        except Exception:
            pass
