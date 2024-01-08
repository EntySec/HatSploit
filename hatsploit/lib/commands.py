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

from hatsploit.core.base.execute import Execute
from hatsploit.core.db.importer import Importer
from hatsploit.lib.modules import Modules
from hatsploit.lib.show import Show
from hatsploit.lib.storage import LocalStorage


class Commands(object):
    """ Subclass of hatsploit.lib module.

    This subclass of hatsploit.lib module is intended for providing
    necessary tools for managing HatSploit commands.
    """

    def __init__(self) -> None:
        super().__init__()

        self.show = Show()

        self.importer = Importer()
        self.execute = Execute()

        self.modules = Modules()
        self.local_storage = LocalStorage()

    def load_commands(self, path: str) -> dict:
        """ Load commands from specified path.

        :param str path: path from which to load commands
        :return dict: loaded commands, names as keys
        and objects as items
        """

        return self.importer.import_commands(path)

    def execute_command(self, command: list) -> None:
        """ Execute command.

        :param list command: command with arguments
        :return None: None
        """

        self.execute.execute_command(command)

    def execute_system_command(self, command: list) -> None:
        """ Execute command as system.

        :param list command: command with arguments
        :return None: None
        """

        self.execute.execute_system(command)

    def execute_custom_command(self, command: list, handler: dict, error: bool = True) -> bool:
        """ Execute command via custom handler.

        Note: handler is a dictionary containing command names as keys and
        command objects as items.

        :param list command: command with arguments
        :param dict handler: handler to use
        :param bool error: True to raise RuntimeError in case of error
        :return bool: status, True if success else False
        :raises RuntimeError: with trailing error message
        """

        if command:
            if not self.execute.execute_builtin_method(command):
                if not self.execute.execute_custom_command(command, handler):
                    if error:
                        raise RuntimeError(f"Unrecognized command: {command[0]}!")
                    return False
        return True

    def execute_custom_plugin_command(self, command: list, plugins: dict, error: bool = True) -> bool:
        """ Execute command via custom plugin.

        Note: plugins is a dictionary containing plugin names as keys and
        plugin objects as items.

        :param list command: command with argument
        :param dict plugins: plugins to use
        :param bool error: True to raise RuntimeError in case of error
        :return bool: status, True if success else False
        :raises RuntimeError: with trailing error message
        """

        if command:
            if not self.execute.execute_builtin_method(command):
                if not self.execute.execute_custom_plugin_command(command, plugins):
                    if error:
                        raise RuntimeError(f"Unrecognized command: {command[0]}!")
                    return False
        return True

    def show_commands(self, handler: dict) -> None:
        """ Print table containing commands from custom handler.

        Note: handler is a dictionary containing command names as keys and
        command objects as items.

        :param dict handler: handler to use
        :return None: None
        """

        self.show.show_custom_commands(handler)

    def commands_completer(self, text: str) -> list:
        """ Commands tab-completion.

        :param str text: text to complete
        :return list: list of completions
        """

        return [command for command in self.get_all_commands() if command.startswith(text)]

    def get_commands(self) -> dict:
        """ Get all imported commands from local storage.

        :return dict: commands, command names as keys and
        command objects as items
        """

        return self.local_storage.get("commands")

    def get_modules_commands(self) -> dict:
        """ Get all commands from loaded modules.

        :return dict: commands, command names as keys and
        command objects as items
        """

        module = self.modules.get_current_module()

        if module:
            return module.commands if hasattr(module, "commands") else {}
        return {}

    def get_plugins_commands(self) -> dict:
        """ Get all commands from loaded plugins.

        :return dict: commands, command names as keys and
        command objects as items
        """

        plugins = self.local_storage.get("loaded_plugins")
        commands = {}

        if plugins:
            for plugin in plugins:
                if hasattr(plugins[plugin], "commands"):
                    for label in plugins[plugin].commands:
                        commands.update(plugins[plugin].commands[label])

        return commands

    def get_all_commands(self) -> dict:
        """ Get all commands, including core commands, module commands
        and plugin commands.

        :return dict: commands, command names as keys and
        command objects as items
        """

        commands = {}
        module = self.modules.get_current_module()

        if module:
            if hasattr(module, "commands"):
                commands.update(module.commands)

        plugins = self.local_storage.get("loaded_plugins")

        if plugins:
            for plugin in plugins:
                if hasattr(plugins[plugin], "commands"):
                    for label in plugins[plugin].commands:
                        commands.update(plugins[plugin].commands[label])

        commands.update(self.local_storage.get("commands"))
        return commands
