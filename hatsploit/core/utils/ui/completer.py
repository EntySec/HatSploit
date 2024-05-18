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

import readline

from pex.string import String
from hatsploit.lib.commands import Commands


class Completer(object):
    """ Subclass of hatsploit.core.utils.ui module.

    This subclass of hatsploit.core.utils.ui module is intended for
    providing a completer for HatSploit CLI interpreter.
    """

    def __init__(self) -> None:
        super().__init__()

        self.string = String()
        self.commands = Commands()

        self.matches = None

    def completer(self, text: str, state: int) -> list:
        """ Tab-completion handler.

        :param str text: text to complete
        :param int state: cursor state
        :return list: matches
        """

        if state == 0:
            options = []
            complete_function = self.default_completer

            original_line = readline.get_line_buffer()
            line = original_line.lstrip()

            stripped = len(original_line) - len(line)
            start_index = readline.get_begidx() - stripped

            if start_index > 0:
                command = self.string.split_args(line)

                if command[0] == "":
                    complete_function = self.default_completer
                else:
                    commands = self.commands.get_commands()

                    other_commands = self.commands.get_modules_commands()
                    other_commands.update(self.commands.get_plugins_commands())

                    if command[0] in commands:
                        if hasattr(commands[command[0]], "complete"):
                            complete_function = commands[command[0]].complete

                        else:
                            if 'Options' in commands[command[0]].details:
                                options = commands[command[0]].details['Options']
                            else:
                                complete_function = self.default_completer

                    elif command[0] in other_commands:
                        if 'Options' in other_commands[command[0]]:
                            options = other_commands[command[0]]['Options']

                        else:
                            complete_function = self.default_completer

                    else:
                        complete_function = self.default_completer
            else:
                complete_function = self.commands.commands_completer

            if options:
                self.matches = self.options_completer(options, text)
            else:
                self.matches = complete_function(text)

        try:
            return self.matches[state]
        except IndexError:
            return []

    @staticmethod
    def options_completer(options: dict, text: str) -> list:
        """ Tab-completion handler for options.

        :param dict options: dictionary, option names as keys and
        option details as items
        :param str text: text to complete
        :return list: matches
        """

        return [option for option in options if option.startswith(text)]

    @staticmethod
    def default_completer(text: str) -> list:
        """ Tab-completion handler for defaults.

        :param str text: text to complete
        :return list: matches
        """

        return []
