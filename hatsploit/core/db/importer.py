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

import os
import importlib.util

from hatsploit.lib.core.module import Module
from hatsploit.lib.core.plugin import Plugin
from hatsploit.lib.core.encoder import Encoder
from hatsploit.lib.core.payload import Payload


class Importer(object):
    """ Subclass of hatsploit.core.db module.

    This subclass of hatsploit.core.db module is intended for
    providing tools for importing HatSploit modules, plugins,
    commands, etc.
    """

    @staticmethod
    def import_payload(payload_path: str) -> Payload:
        """ Import payload from path.

        :param str payload_path: path to payload
        :return Payload: payload object
        :raises RuntimeError: with trailing error message
        """

        try:
            if not payload_path.endswith('.py'):
                payload_path = payload_path + '.py'

            spec = importlib.util.spec_from_file_location(payload_path, payload_path)
            payload = importlib.util.module_from_spec(spec)

            spec.loader.exec_module(payload)
            payload = payload.HatSploitPayload()

        except Exception as e:
            raise RuntimeError(f"Failed to import payload: {str(e)}!")

        return payload

    @staticmethod
    def import_encoder(encoder_path: str) -> Encoder:
        """ Import encoder from path.

        :param str encoder_path: path to encoder
        :return Encoder: encoder object
        :raises RuntimeError: with trailing error message
        """

        try:
            if not encoder_path.endswith('.py'):
                encoder_path = encoder_path + '.py'

            spec = importlib.util.spec_from_file_location(encoder_path, encoder_path)
            encoder = importlib.util.module_from_spec(spec)

            spec.loader.exec_module(encoder)
            encoder = encoder.HatSploitEncoder()

        except Exception as e:
            raise RuntimeError(f"Failed to import encoder: {str(e)}!")

        return encoder

    @staticmethod
    def import_module(module_path: str) -> Module:
        """ Import module from path.

        :param str module_path: path to module
        :return Module: module object
        :raises RuntimeError: with trailing error message
        """

        try:
            if not module_path.endswith('.py'):
                module_path = module_path + '.py'

            spec = importlib.util.spec_from_file_location(module_path, module_path)
            module = importlib.util.module_from_spec(spec)

            spec.loader.exec_module(module)
            module = module.HatSploitModule()

        except Exception as e:
            raise RuntimeError(f"Failed to import module: {str(e)}!")

        return module

    @staticmethod
    def import_plugin(plugin_path: str) -> Plugin:
        """ Import plugin from path.

        :param str plugin_path: path to plugin
        :return Plugin: plugin object
        :raises RuntimeError: with trailing error message
        """

        try:
            if not plugin_path.endswith('.py'):
                plugin_path = plugin_path + '.py'

            spec = importlib.util.spec_from_file_location(plugin_path, plugin_path)
            plugin = importlib.util.module_from_spec(spec)

            spec.loader.exec_module(plugin)
            plugin = plugin.HatSploitPlugin()

        except Exception as e:
            raise RuntimeError(f"Failed to import plugin: {str(e)}!")

        return plugin
