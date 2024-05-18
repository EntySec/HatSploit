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

from typing import Optional
from textwrap import dedent

from badges import Badges, Tables

from hatsploit.lib.encoders import Encoders
from hatsploit.lib.jobs import Jobs
from hatsploit.lib.loot import Loot
from hatsploit.lib.modules import Modules
from hatsploit.lib.module import Module
from hatsploit.lib.payloads import Payloads
from hatsploit.lib.plugins import Plugins
from hatsploit.lib.sessions import Sessions
from hatsploit.lib.storage import LocalStorage


class Show(object):
    """ Subclass of hatsploit.lib module.

    This subclass of hatsploit.lib module is intended for providing
    tools for showing different things.
    """

    def __init__(self) -> None:
        super().__init__()

        self.jobs = Jobs()
        self.loot = Loot()
        self.local_storage = LocalStorage()
        self.modules = Modules()
        self.payloads = Payloads()
        self.plugins = Plugins()
        self.encoders = Encoders()
        self.sessions = Sessions()

        self.tables = Tables()
        self.badges = Badges()

    def show_custom_commands(self, commands: dict) -> None:
        """ Show custom commands.

        Note: commands is a dictionary containing command names as keys and
        command objects as items.

        :param dict commands: commands
        :return None: None
        """

        data = {}
        headers = ("Command", "Description")

        for command in sorted(commands):
            data[commands[command].details['Category']] = []

        for command in sorted(commands):
            data[commands[command].details['Category']].append(
                (command, commands[command].details['Description'])
            )

        for label in sorted(data):
            self.tables.print_table(f"{label} Commands", headers, *data[label])

    def show_interface_commands(self) -> None:
        """ Show interface commands.

        :return None: None
        :raises RuntimeWarning: with trailing warning message
        """

        if not self.local_storage.get("commands"):
            raise RuntimeWarning("No commands available.")

        self.show_custom_commands(self.local_storage.get("commands"))

    def show_plugin_commands(self, plugins: dict) -> None:
        """ Show all plugins commands.

        Note: plugins is a dictionary containing plugin names as keys and
        plugin objects as items.

        :param dict plugins: plugins
        :return None: None
        """

        for plugin in plugins:
            plugin = plugins[plugin]

            if not hasattr(plugin, "commands"):
                continue

            data = {}
            headers = ("Command", "Description")
            commands = plugin.commands

            for label in sorted(commands):
                data[label] = []

                for command in sorted(commands[label]):
                    data[label].append(
                        (command, commands[label][command]['Description'])
                    )

            for label in sorted(data):
                self.tables.print_table(f"{label} Commands", headers, *data[label])

    def show_module_commands(self, module: Module) -> None:
        """ Show current module commands.

        :param Module module: module object
        :return None: None
        """

        if not hasattr(module, "commands"):
            return

        data = []
        headers = ("Command", "Description")
        commands = module.commands

        for command in sorted(commands):
            data.append(
                (command, commands[command]['Description'])
            )

        self.tables.print_table("Module Commands", headers, *data)

    def show_all_commands(self) -> None:
        """ Show all commands.

        :return None: None
        """

        self.show_interface_commands()

        if self.modules.get_current_module():
            self.show_module_commands(
                self.modules.get_current_module())

        if self.plugins.get_loaded_plugins():
            self.show_plugin_commands(
                self.plugins.get_loaded_plugins())

    def show_jobs(self, jobs: dict) -> None:
        """ Show active jobs.

        :param dict jobs: dictionary of jobs, where job IDs are keys
        and job objects are items
        :return None: None
        :raises RuntimeWarning: with trailing warning message
        """

        if not jobs:
            raise RuntimeWarning("No running jobs available.")

        data = []
        headers = ("ID", "Name", "Module")

        for job_id, job in jobs.items():
            data.append(
                (job_id, job['Name'], job['Module'])
            )

        self.tables.print_table("Active Jobs", headers, *data)

    def show_sessions(self, sessions: dict) -> None:
        """ Show opened sessions.

        :param dict sessions: sessions dictionary, where session ID is a key
        and session data is item
        :return None: None
        :raises RuntimeWarning: with trailing warning message
        """

        if not sessions:
            raise RuntimeWarning("No opened sessions available.")

        data = []
        headers = ("ID", "Platform", "Arch", "Type", "Host", "Port")

        for session_id, session in sessions.items():
            data.append(
                (session_id, session['Platform'], session['Arch'],
                 session['Type'], session['Host'], session['Port'])
            )

        self.tables.print_table("Opened Sessions", headers, *data)

    def show_loot(self, loot: list) -> None:
        """ Show collected loot.

        :param list loot: loot array
        (array of tuples containing loot information)
        :return None: None
        :raises RuntimeWarning: with trailing warning message
        """

        if not loot:
            raise RuntimeWarning("No loot collected yet.")

        headers = ("Loot", "Path", "Time")
        self.tables.print_table("Collected Loot", headers, *loot)

    def show_module_databases(self, databases: dict) -> None:
        """ Show connected module databases.

        :param dict databases: module databases
        :return None: None
        :raises RuntimeWarning: with trailing warning message
        """

        if not databases:
            raise RuntimeWarning("No module databases connected.")

        data = []
        number = 0
        headers = ("Number", "Name", "Path")

        for name in databases:
            data.append(
                (number, name, databases[name]['Path'])
            )
            number += 1

        self.tables.print_table("Connected Module Databases", headers, *data)

    def show_payload_databases(self, databases: dict) -> None:
        """ Show connected payload databases.

        :param dict databases: payload databases
        :return None: None
        :raises RuntimeWarning: with trailing warning message
        """

        if not databases:
            raise RuntimeWarning("No payload databases connected.")

        data = []
        number = 0
        headers = ("Number", "Name", "Path")

        for name in databases:
            data.append(
                (number, name, databases[name]['Path'])
            )
            number += 1

        self.tables.print_table("Connected Payload Databases", headers, *data)

    def show_encoder_databases(self, databases: dict) -> None:
        """ Show connected encoder databases.

        :param dict databases: encoder databases
        :return None: None
        :raises RuntimeWarning: with trailing warning message
        """

        if not databases:
            raise RuntimeWarning("No encoder databases connected.")

        data = []
        number = 0
        headers = ("Number", "Name", "Path")

        for name in databases:
            data.append(
                (number, name, databases[name]['Path'])
            )
            number += 1

        self.tables.print_table("Connected Encoder Databases", headers, *data)

    def show_plugin_databases(self, databases: dict) -> None:
        """ Show connected plugin databases.

        :param dict databases: plugin databases
        :return None: None
        :raises RuntimeWarning: with trailing warning message
        """

        if not databases:
            raise RuntimeWarning("No plugin databases connected.")

        data = []
        number = 0
        headers = ("Number", "Name", "Path")

        for name in databases:
            data.append(
                (number, name, databases[name]['Path'])
            )
            number += 1

        self.tables.print_table("Connected Plugin Databases", headers, *data)

    def show_loaded_plugins(self, plugins: dict) -> None:
        """ Show loaded plugins.

        :param dict plugins: dictionary of plugins, where plugin name is a key
        and plugin object is an item
        :return None: None
        :raises RuntimeWarning: with trailing warning message
        """

        headers = ("Number", "Plugin", "Name")
        shorts = {}
        data = []
        number = 0

        for plugin in sorted(plugins):
            data.append(
                (number, plugin, plugin[plugin].details['Name'])
            )

            shorts.update({
                number: plugin
            })
            number += 1

        if not shorts:
            raise RuntimeWarning("No plugins available.")

        self.tables.print_table(f"Loaded Plugins", headers, *data)
        self.local_storage.set("plugin_shorts", shorts)

    def show_plugins(self, plugins: dict) -> None:
        """ Show plugins.

        :param dict plugins: dictionary of plugins, where plugin name is a key
        and plugin data is an item
        :return None: None
        :raises RuntimeWarning: with trailing warning message
        """

        headers = ("Number", "Plugin", "Name")
        shorts = {}
        number = 0

        for database in sorted(plugins):
            db_plugins = plugins[database]
            data = []

            for plugin in sorted(db_plugins):
                plugin = db_plugins[plugin]

                data.append(
                    (number, plugin['Plugin'], plugin['Name'])
                )

                shorts.update({
                    number: plugin['Plugin']
                })

                number += 1

            self.tables.print_table(f"Plugins ({database})", headers, *data)

        if not shorts:
            raise RuntimeWarning("No plugins available.")

        self.local_storage.set("plugin_shorts", shorts)

    def show_encoders(self, encoders: dict) -> None:
        """ Show encoders.

        :param dict encoders: dictionary of encoders, where encoder name is a key
        and encoder data is an item
        :return None: None
        :raises RuntimeWarning: with trailing warning message
        """

        headers = ("Number", "Encoder", "Name")
        shorts = {}
        number = 0

        for database in sorted(encoders):
            db_encoders = encoders[database]
            data = []

            for encoder in sorted(db_encoders):
                encoder = db_encoders[encoder]

                data.append(
                    (number, encoder['Encoder'], encoder['Name'])
                )

                shorts.update({
                    number: encoder['Encoder']
                })

                number += 1

            self.tables.print_table(f"Encoders ({database})", headers, *data)

        if not shorts:
            raise RuntimeWarning("No encoders available.")

        self.local_storage.set("encoder_shorts", shorts)

    def show_modules(self, modules: dict, category: Optional[str] = None) -> None:
        """ Show modules by category.

        :param dict modules: modules dictionary, module name as key and
        module data as item
        :param Optional[str] category: category
        :return None: None
        :raises RuntimeWarning: with trailing warning message
        """

        headers = ("Number", "Category", "Module", "Rank", "Name")
        shorts = {}
        number = 0

        for database in sorted(modules):
            db_modules = modules[database]
            data = []

            for module in sorted(db_modules):
                module = db_modules[module]

                if not category:
                    data.append(
                        (number, module['Category'], module['Module'],
                         module['Rank'], module['Name'])
                    )

                    shorts.update(
                        {number: module['Module']}
                    )

                    number += 1
                    continue

                if category == module['Category']:
                    data.append(
                        (number, module['Category'], module['Module'],
                         module['Rank'], module['Name'])
                    )

                    shorts.update({
                        number: module['Module']
                    })

                    number += 1

            if category:
                self.tables.print_table(f"{category.title()} Modules ({database})", headers, *data)
            else:
                self.tables.print_table(f"Modules ({database})", headers, *data)

        if not shorts:
            raise RuntimeWarning("No modules available.")

        self.local_storage.set("module_shorts", shorts)

    def show_payloads(self, payloads: dict) -> None:
        """ Show payloads.

        :param dict payloads: payloads dictionary, payload name as key
        and payload data as item
        :return None: None
        :raises RuntimeWarning: with trailing warning message
        """

        headers = ("Number", "Payload", "Rank", "Name")
        shorts = {}
        number = 0

        for database in sorted(payloads):
            db_payloads = payloads[database]
            data = []

            for payload in sorted(db_payloads):
                payload = db_payloads[payload]

                data.append(
                    (number, payload['Payload'], payload['Rank'],
                     payload['Name'])
                )

                shorts.update({
                    number: payload['Payload']
                })

                number += 1

            self.tables.print_table(f"Payloads ({database})", headers, *data)

        if not shorts:
            raise RuntimeWarning("No payloads available.")

        self.local_storage.set("payload_shorts", shorts)

    def show_search_plugins(self, plugins: dict, keyword: str) -> None:
        """ Show plugins that contain the keyword.

        :param dict plugins: dictionary of plugins, where plugin name is a key
        and plugin data is an item
        :param str keyword: keyword
        :return None: None
        """

        headers = ("Number", "Plugin", "Name")
        shorts = {}
        number = 0

        for database in plugins:
            db_plugins = plugins[database]
            data = []

            for plugin in sorted(db_plugins):
                plugin = db_plugins[plugin]

                if keyword not in plugin['Plugin'] + plugin['Name']:
                    continue

                data.append(
                    (number, plugin['Plugin'].replace(keyword, f'%red{keyword}%end'),
                     plugin['Name'].replace(keyword, f'%red{keyword}%end'))
                )

                shorts.update(
                    {number: plugin['Plugin']}
                )

                number += 1

            if data:
                self.tables.print_table(f"Plugins ({database})", headers, *data)

        if shorts:
            self.local_storage.set("plugin_shorts", shorts)

    def show_search_encoders(self, encoders: dict, keyword: str) -> None:
        """ Show encoders that contain the keyword.

        :param dict encoders: dictionary of encoders, where encoder name is a key
        and encoder data is an item
        :param str keyword: keyword
        :return None: None
        """

        headers = ("Number", "Encoder", "Name")
        shorts = {}
        number = 0

        for database in encoders:
            db_encoders = encoders[database]
            data = []

            for encoder in sorted(db_encoders):
                encoder = db_encoders[encoder]

                if keyword not in encoder['Encoder'] + encoder['Name']:
                    continue

                data.append(
                    (number, encoder['Encoder'].replace(keyword, f'%red{keyword}%end'),
                     encoder['Name'].replace(keyword, f'%red{keyword}%end'))
                )

                shorts.update(
                    {number: encoder['Encoder']}
                )

                number += 1

            if data:
                self.tables.print_table(f"Encoders ({database})", headers, *data)

        if shorts:
            self.local_storage.set("encoder_shorts", shorts)

    def show_search_modules(self, modules: dict, keyword: str) -> None:
        """ Show modules that contain the keyword.

        :param dict modules: dictionary of modules, where module name is a key
        and module data is an item
        :param str keyword: keyword
        :return None: None
        """

        headers = ("Number", "Category", "Module", "Rank", "Name")
        shorts = {}
        number = 0

        for database in modules:
            db_modules = modules[database]
            data = []

            for module in sorted(db_modules):
                module = db_modules[module]

                if keyword not in module['Module'] + module['Name']:
                    continue

                data.append(
                    (number, module['Category'],
                     module['Module'].replace(keyword, f'%red{keyword}%end'),
                     module['Rank'],
                     module['Name'].replace(keyword, f'%red{keyword}%end'))
                )

                shorts.update(
                    {number: module['Module']}
                )

                number += 1

            if data:
                self.tables.print_table(f"Modules ({database})", headers, *data)

        if shorts:
            self.local_storage.set("module_shorts", shorts)

    def show_search_payloads(self, payloads: dict, keyword: str) -> None:
        """ Show payloads that contain the keyword.

        :param dict payloads: dictionary of payloads, where payload name is a key
        and payload data is an item
        :param str keyword: keyword
        :return None: None
        """

        headers = ("Number", "Module", "Rank", "Name")
        shorts = {}
        number = 0

        for database in payloads:
            db_payloads = payloads[database]
            data = []

            for payload in sorted(db_payloads):
                payload = db_payloads[payload]

                if keyword not in payload['Payload'] + payload['Name']:
                    continue

                data.append(
                    (number,
                     payload['Payload'].replace(keyword, f'%red{keyword}%end'),
                     payload['Rank'],
                     payload['Name'].replace(keyword, f'%red{keyword}%end'))
                )

                shorts.update(
                    {number: payload['Payload']}
                )

                number += 1

            if data:
                self.tables.print_table(f"Payloads ({database})", headers, *data)

        if shorts:
            self.local_storage.set("payload_shorts", shorts)

    def show_module_information(self, details: Optional[dict] = None) -> None:
        """ Show module details.

        :param Optional[dict] details: module details
        :return None: None
        """

        if not details:
            module = self.modules.get_current_module()
            details = module.details

        self.badges.print_empty(dedent(f"""
            Category:    {details['Category']}
            Name:        {details['Name']}
            Module:      {details['Module']}
            Description: {details['Description']}
            Platform:    {str(details['Platform'])}
            Rank:        {details['Rank']}
        """))

    def show_options_table(self, title: str, options: dict) -> None:
        """ Show options for specific title.

        :param str title: title
        :param dict options: options, option names as keys and option data as
        items
        :return None: None
        """

        headers = ("Option", "Value", "Required", "Description")
        data = []

        for option in sorted(options):
            if not options[option]['Visible']:
                continue

            value, required = options[option]['Value'], \
                options[option]['Required']

            required = "yes" if required else "no"
            value = "" if value is None else value

            if isinstance(value, bool):
                value = "yes" if value else "no"

            data.append(
                (option, value, required,
                 options[option]['Description'])
            )

        self.tables.print_table(title, headers, *data)

    def show_options(self, module: Module) -> None:
        """ Show options.

        :param Module module: module object
        :return None: None
        :raises RuntimeWarning: with trailing warning message
        """

        payload = self.payloads.get_current_payload(module)

        if not module:
            raise RuntimeWarning("No module selected.")

        if hasattr(module, "options"):
            self.show_options_table(
                f"Module Options ({module.details['Module']})", module.options)

        if not payload:
            return

        encoder = self.encoders.get_current_encoder(module, payload)

        if hasattr(payload, "options"):
            self.show_options_table(
                f"Payload Options ({payload.details['Payload']})", payload.options)

        if encoder and hasattr(encoder, "options"):
            self.show_options_table(
                f"Encoder Options ({encoder.details['Encoder']})", encoder.options)

    def show_advanced(self, module: Module) -> None:
        """ Show advanced options.

        :param Module module: module object
        :return None: None
        :raises RuntimeWarning: with trailing warning message
        """

        payload = self.payloads.get_current_payload(module)

        if not module:
            raise RuntimeWarning("No module selected.")

        if hasattr(module, "advanced"):
            self.show_options_table(
                f"Module Advanced Options ({module.details['Module']})", module.advanced)

        if not payload:
            return

        encoder = self.encoders.get_current_encoder(module, payload)

        if hasattr(payload, "advanced"):
            self.show_options_table(
                f"Payload Advanced Options ({payload.details['Payload']})", payload.advanced)

        if encoder and hasattr(encoder, "advanced"):
            self.show_options_table(
                f"Encoder Advanced Options ({encoder.details['Encoder']})", encoder.advanced)
