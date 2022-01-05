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

from hatsploit.lib.modules import Modules
from hatsploit.lib.payloads import Payloads
from hatsploit.lib.storage import LocalStorage

from hatsploit.utils.tcp import TCPClient


class Options:
    modules = Modules()
    payloads = Payloads()
    local_storage = LocalStorage()

    handler_options = {
        'Module': {
            'BLINDER': {
                'Description': 'Use Blinder.',
                'Value': 'yes',
                'Type': "boolean",
                'Required': True
            },
            'PAYLOAD': {
                'Description': 'Payload to use.',
                'Value': None,
                'Type': "payload",
                'Required': False
            },
            'LHOST': {
                'Description': "Local host to listen on.",
                'Value': "0.0.0.0",
                'Type': "ip",
                'Required': True
            },
            'LPORT': {
                'Description': "Local port to listen on.",
                'Value': 8888,
                'Type': "port",
                'Required': True
            },
            'RPORT': {
                'Description': "Remote port to connect.",
                'Value': 8888,
                'Type': "port",
                'Required': True
            }
        },
        'Payload': {
            'RHOST': {
                'Description': "Remote host to connect.",
                'Value': TCPClient.get_local_host(),
                'Type': "ip",
                'Required': True
            },
            'RPORT': {
                'Description': "Remote port to connect.",
                'Value': 8888,
                'Type': "port",
                'Required': True
            },
            'BPORT': {
                'Description': "Port to bind to.",
                'Value': 8888,
                'Type': "port",
                'Required': True
            }
        }
    }

    @staticmethod
    def remove_options(target, options):
        for option in list(target.options):
            if option.lower() in options:
                target.options.pop(option)

    @staticmethod
    def check_options(target):
        if not hasattr(target, "options"):
            return False
        if not isinstance(target.options, dict):
            return False
        return True

    def add_handler_options(self):
        if self.modules.check_current_module():
            current_module = self.modules.get_current_module_object()

            if hasattr(current_module, "payload"):
                blinder_option = 'blinder'.upper()
                payload_option = 'payload'.upper()

                handler_options = self.handler_options
                saved_handler_options = self.local_storage.get("handler_options")

                if not saved_handler_options:
                    saved_handler_options = {
                        'Module': {
                        },
                        'Payload': {
                        }
                    }

                module = self.modules.get_current_module_name()
                current_payload = self.payloads.get_current_payload()

                if module not in saved_handler_options['Module']:
                    saved_handler_options['Module'][module] = handler_options['Module']

                if not self.check_options(current_module):
                    current_module.options = {}

                current_module.options.update(saved_handler_options['Module'][module])
                current_module.options[payload_option]['Value'] = current_module.payload['Value']

                if not current_payload:
                    current_module.options[blinder_option]['Value'] = 'yes'
                    current_module.options[blinder_option]['Required'] = True
                else:
                    current_module.options[blinder_option]['Value'] = 'no'
                    current_module.options[blinder_option]['Required'] = False

                if 'Blinder' in current_module.payload:
                    if not current_module.payload['Blinder']:
                        current_module.options.pop(blinder_option)

                if blinder_option in current_module.options and not current_payload:
                    if current_module.options[blinder_option]['Value'].lower() in ['yes', 'y']:
                        current_module.payload['Value'] = None

                        current_module.options[payload_option]['Value'] = None
                        current_module.options[payload_option]['Required'] = False
                    else:
                        current_module.options[payload_option]['Required'] = True
                else:
                    current_module.options[payload_option]['Required'] = True

                if current_payload:
                    payload = current_module.payload['Value']

                    if payload not in saved_handler_options['Payload']:
                        saved_handler_options['Payload'][payload] = handler_options['Payload']

                    if not self.check_options(current_payload):
                        current_payload.options = {}

                    current_payload.options.update(saved_handler_options['Payload'][payload])

                    if 'Handler' in current_module.payload:
                        special = current_module.payload['Handler']
                    else:
                        special = []

                    if current_payload.details['Type'] == 'reverse_tcp':
                        if special != 'bind_tcp':
                            self.remove_options(current_module, ['rport'])
                            self.remove_options(current_payload, ['bport'])

                    elif current_payload.details['Type'] == 'bind_tcp':
                        if special != 'reverse_tcp':
                            self.remove_options(current_module, ['lhost', 'lport'])
                            self.remove_options(current_payload, ['rhost', 'rport'])

                    else:
                        if special == 'reverse_tcp':
                            self.remove_options(current_module, ['lhost', 'lport'])
                            self.remove_options(current_payload, ['rhost', 'rport'])

                        if special == 'bind_tcp':
                            self.remove_options(current_module, ['rport'])
                            self.remove_options(current_payload, ['bport'])
                else:
                    self.remove_options(current_module, self.handler_options['Module'])

                for option in current_module.options:
                    if option.lower() in self.handler_options['Module']:
                        saved_handler_options['Module'][module][option]['Value'] = current_module.options[option]['Value']

                current_module.handler = {}
                for option in saved_handler_options['Module'][module]:
                    current_module.handler.update({option: saved_handler_options['Module'][module][option]['Value']})

                if current_payload:
                    payload = current_module.payload['Value']

                    for option in current_payload.options:
                        if option.lower() in self.handler_options['Payload']:
                            saved_handler_options['Payload'][payload][option]['Value'] = current_payload.options[option]['Value']

                    current_payload.handler = {}
                    for option in saved_handler_options['Payload'][payload]:
                        current_payload.handler.update({option: saved_handler_options['Payload'][payload][option]['Value']})

                self.local_storage.set("handler_options", saved_handler_options)
