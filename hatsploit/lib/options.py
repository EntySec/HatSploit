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

import copy

from typing import Union

from pex.proto.tcp import TCPTools

from hatsploit.lib.payload import Payload
from hatsploit.lib.module import Module

from hatsploit.lib.storage import LocalStorage


class Options(object):
    """ Subclass of hatsploit.lib module.

    This subclass of hatsploit.lib module is intended for
    providing tools for working with module/payload options.
    """

    def __init__(self) -> None:
        super().__init__()

        self.local_storage = LocalStorage()

        self.handler_options = {
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
                'RBHOST': {
                    'Description': "Remote bind host to connect.",
                    'Value': None,
                    'Type': "ip",
                    'Required': True
                },
                'RBPORT': {
                    'Description': "Remote bind port to connect.",
                    'Value': 8888,
                    'Type': "port",
                    'Required': True
                }
            },
            'Payload': {
                'ENCODER': {
                    'Description': 'Encoder to use.',
                    'Value': None,
                    'Type': "encoder",
                    'Required': False
                },
                'RHOST': {
                    'Description': "Remote host to connect.",
                    'Value': TCPTools.get_local_host(),
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
    def remove_options(target: dict, options: list) -> None:
        """ Remove options by names from target dictionary.

        :param dict target: target dictionary
        :param list options: list of option names
        :return None: None
        """

        for option in list(target):
            if option.upper() in options:
                target.pop(option)

    @staticmethod
    def check_options(target: Union[Module, Payload]) -> bool:
        """ Check if module object or payload object has options instance.

        :param Union[Module, Payload] target: payload object or module object
        :return bool: True if instance found else False
        """

        if not hasattr(target, "options"):
            return False

        if not isinstance(target.options, dict):
            return False

        return True

    def add_handler_options(self, module: Module, payload: Payload) -> None:
        """ Add handler options to the module object and payload object.

        :param Module module: module object
        :param Payload payload: payload object
        :return None: None
        """

        if module:
            if hasattr(module, "payload"):
                blinder_option = 'blinder'.upper()
                payload_option = 'payload'.upper()

                handler_options = copy.deepcopy(self.handler_options)
                saved_handler_options = self.local_storage.get("handler_options")

                if not saved_handler_options:
                    saved_handler_options = {
                        'Module': {
                        },
                        'Payload': {
                        }
                    }

                module_name = module.details['Module']

                if module_name not in saved_handler_options['Module']:
                    saved_handler_options['Module'][module_name] = handler_options['Module']

                if not self.check_options(module):
                    module.options = {}

                module.options.update(saved_handler_options['Module'][module_name])
                module.options[payload_option]['Value'] = module.payload['Value']

                if not payload:
                    module.options[blinder_option]['Value'] = 'yes'
                    module.options[blinder_option]['Required'] = True
                else:
                    module.options[blinder_option]['Value'] = 'no'
                    module.options[blinder_option]['Required'] = False

                if 'Blinder' in module.payload:
                    if not module.payload['Blinder']:
                        module.options.pop(blinder_option)

                if blinder_option in module.options and not payload:
                    if module.options[blinder_option]['Value'].lower() in ['yes', 'y']:
                        module.payload['Value'] = None

                        module.options[payload_option]['Value'] = None
                        module.options[payload_option]['Required'] = False
                    else:
                        module.options[payload_option]['Required'] = True
                else:
                    module.options[payload_option]['Required'] = True

                if 'Handler' in module.payload:
                    special = module.payload['Handler']
                else:
                    special = ''

                if payload:
                    payload_name = module.payload['Value']

                    if payload_name not in saved_handler_options['Payload']:
                        saved_handler_options['Payload'][payload_name] = handler_options['Payload']

                    if not self.check_options(payload):
                        payload.options = {}

                    payload.options.update(saved_handler_options['Payload'][payload_name])

                    if payload.details['Type'] == 'reverse_tcp':
                        if special != 'bind_tcp':
                            self.remove_options(module.options, ['RBHOST', 'RBPORT'])
                            self.remove_options(payload.options, ['BPORT'])

                    elif payload.details['Type'] == 'bind_tcp':
                        if special != 'reverse_tcp':
                            self.remove_options(module.options, ['LHOST', 'LPORT'])
                            self.remove_options(payload.options, ['RHOST', 'RPORT'])

                    else:
                        self.remove_options(payload.options, ['RHOST', 'RPORT', 'BPORT'])

                        if special != 'reverse_tcp':
                            self.remove_options(module.options, ['LHOST', 'LPORT'])

                        if special != 'bind_tcp':
                            self.remove_options(module.options, ['RBHOST', 'RBPORT'])
                else:
                    if special != 'reverse_tcp':
                        self.remove_options(module.options, ['LHOST', 'LPORT'])

                    if special != 'bind_tcp':
                        self.remove_options(module.options, ['RBHOST', 'RBPORT'])

                for option in module.options:
                    if option.upper() in handler_options['Module']:
                        saved_handler_options['Module'][module_name][option]['Value'] = \
                            module.options[option]['Value']

                module.handler = {}
                for option in saved_handler_options['Module'][module_name]:
                    module.handler.update({option: saved_handler_options['Module'][module_name][option]['Value']})

                if payload:
                    payload_name = module.payload['Value']

                    for option in payload.options:
                        if option.upper() in handler_options['Payload']:
                            saved_handler_options['Payload'][payload_name][option]['Value'] = \
                                payload.options[option]['Value']

                    payload.handler = {}
                    for option in saved_handler_options['Payload'][payload_name]:
                        value = saved_handler_options['Payload'][payload_name][option]['Value']

                        payload.handler.update({option: value})
                        module.handler.update({option: value})

                    for option in saved_handler_options['Module'][module_name]:
                        payload.handler.update({
                            option: saved_handler_options['Module'][module_name][option]['Value']
                        })

                self.local_storage.set("handler_options", saved_handler_options)

    def add_payload_handler(self, payload: Payload) -> None:
        """ Add handler options to the payload.

        :param Payload payload: payload object
        :return None: None
        """

        handler_options = {}
        payload.handler = {}

        handler_options.update(self.handler_options['Payload'])

        if payload.details['Type'] == 'reverse_tcp':
            self.remove_options(handler_options, ['BPORT'])
        elif payload.details['Type'] == 'bind_tcp':
            self.remove_options(handler_options, ['RHOST', 'RPORT'])
        else:
            self.remove_options(handler_options, ['RHOST', 'RPORT', 'BPORT'])

        for option in handler_options:
            payload.handler.update({option: handler_options[option]['Value']})
