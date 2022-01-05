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

from hatsploit.utils.tcp import TCPClient

from hatsploit.lib.modules import Modules
from hatsploit.lib.payloads import Payloads


class Options:
    modules = Modules()
    payloads = Payloads()

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
            'RBPORT': {
                'Description': "Remote bind port.",
                'Value': 8888,
                'Type': "port",
                'Required': True
            }
        },
        'Payload': {
            'CBHOST': {
                'Description': "Connect-back host.",
                'Value': TCPClient.get_local_host(),
                'Type': "ip",
                'Required': True
            },
            'CBPORT': {
                'Description': "Connect-back port.",
                'Value': 8888,
                'Type': "port",
                'Required': True
            },
            'BPORT': {
                'Description': "Bind port.",
                'Value': 8888,
                'Type': "port",
                'Required': True
            }
        }
    }

    def remove_options(self, target, options):
        for option in list(target.options):
            if option.lower() in options:
                target.options.pop(option)

    def add_handler_options(self):
        if self.modules.check_current_module():
            current_module = self.modules.get_current_module_object()

            if hasattr(current_module, "payload"):
                blinder_option = 'blinder'.upper()
                payload_option = 'payload'.upper()

                handler_options = HandlerOptions

                module = self.modules.get_current_module_name()
                current_payload = self.payloads.get_current_payload()

                if module not in self.handler_options['Module']:
                    self.handler_options['Module'][module] = handler_options['Module']

                if not hasattr(current_module, "options"):
                    current_module.options = {}

                current_module.options.update(self.handler_options['Module'][module])
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

                    if payload not in self.handler_options['Payload']:
                        self.handler_options['Payload'][payload] = handler_options['Payload']

                    if not hasattr(current_payload, "options"):
                        current_payload.options = {}

                    current_payload.options.update(self.handler_options['Payload'][payload])

                    if 'Handler' in current_module.payload:
                        special = current_module.payload['Handler']
                    else:
                        special = []

                    if current_payload.details['Type'] == 'reverse_tcp':
                        if 'bind_tcp' not in special:
                            self.remove_options(current_module, ['rbhost'])
                            self.remove_options(current_payload, ['bport'])

                    elif current_payload.details['Type'] == 'bind_tcp':
                        if 'reverse_tcp' not in special:
                            self.remove_options(current_module, ['lhost', 'lport'])
                            self.remove_options(current_payload, ['cbhost', 'cbport'])

                    else:
                        if 'reverse_tcp' not in special:
                            self.remove_options(current_module, ['lhost', 'lport'])
                            self.remove_options(current_payload, ['cbhost', 'cbport'])

                        if 'bind_tcp' not in special:
                            self.remove_options(current_module, ['rbhost'])
                            self.remove_options(current_payload, ['bport'])
                else:
                    self.remove_options(current_module, ['lhost', 'lport', 'rbhost'])

                for option in current_module.options:
                    if option.lower() in ['lhost', 'lport', 'rbport', 'payload', 'blinder']:
                        self.handler_options['Module'][module][option]['Value'] = current_module.options[option]['Value']

                current_module.handler = self.handler_options['Module'][module]

                if current_payload:
                    for option in current_payload.options:
                        if option.lower() in ['cbhost', 'cbport', 'bport']:
                            self.handler_options['Payload'][payload][option]['Value'] = current_payload.options[option]['Value']

                    current_payload.handler = self.handler_options['Payload'][payload]
