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

from hatsploit.core.cli.colors import Colors
from hatsploit.core.cli.tables import Tables
from hatsploit.core.cli.badges import Badges
from hatsploit.lib.encoders import Encoders
from hatsploit.lib.jobs import Jobs
from hatsploit.lib.loot import Loot
from hatsploit.lib.modules import Modules
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

        self.colors = Colors()
        self.tables = Tables()
        self.badges = Badges()

    def show_custom_commands(self, commands: dict) -> None:
        """ Show custom commands.

        Note: commands is a dictionary containing command names as keys and
        command objects as items.

        :param dict commands: commands
        :return None: None
        """

        commands_data = {}
        headers = ("Command", "Description")

        for command in sorted(commands):
            label = commands[command].details['Category']
            commands_data[label] = []

        for command in sorted(commands):
            label = commands[command].details['Category']
            commands_data[label].append(
                (command, commands[command].details['Description'])
            )

        for label in sorted(commands_data):
            self.tables.print_table(label.title() + " Commands", headers, *commands_data[label])

    def show_interface_commands(self) -> None:
        """ Show interface commands.

        :return None: None
        :raises RuntimeWarning: with trailing warning message
        """

        if self.local_storage.get("commands"):
            self.show_custom_commands(self.local_storage.get("commands"))
        else:
            raise RuntimeWarning("No commands available.")

    def show_plugin_commands(self) -> None:
        """ Show all loaded plugin commands.

        :return None: None
        """

        plugins = self.plugins.get_loaded_plugins()

        for plugin in plugins:
            plugin = plugins[plugin]

            if hasattr(plugin, "commands"):
                commands_data = {}
                headers = ("Command", "Description")
                commands = plugin.commands

                for label in sorted(commands):
                    commands_data[label] = []

                    for command in sorted(commands[label]):
                        commands_data[label].append(
                            (command, commands[label][command]['Description'])
                        )

                for label in sorted(commands_data):
                    self.tables.print_table(label.title() + " Commands", headers, *commands_data[label])

    def show_module_commands(self) -> None:
        """ Show current module commands.

        :return None: None
        """

        module = self.modules.get_current_module()

        if hasattr(module, "commands"):
            commands_data = []
            headers = ("Command", "Description")
            commands = module.commands

            for command in sorted(commands):
                commands_data.append(
                    (command, commands[command]['Description'])
                )

            self.tables.print_table("Module Commands", headers, *commands_data)

    def show_all_commands(self) -> None:
        """ Show all commands.

        :return None: None
        """

        self.show_interface_commands()

        if self.modules.get_current_module():
            self.show_module_commands()

        if self.plugins.get_loaded_plugins():
            self.show_plugin_commands()

    def show_jobs(self) -> None:
        """ Show active jobs.

        :return None: None
        :raises RuntimeWarning: with trailing warning message
        """

        jobs = self.jobs.get_jobs()

        if jobs:
            jobs_data = []
            headers = ("ID", "Name", "Module")

            for job_id in jobs:
                jobs_data.append(
                    (job_id, jobs[job_id]['Name'], jobs[job_id]['Module'])
                )

            self.tables.print_table("Active Jobs", headers, *jobs_data)
        else:
            raise RuntimeWarning("No running jobs available.")

    def show_loot(self) -> None:
        """ Show collected loot.

        :return None: None
        :raises RuntimeWarning: with trailing warning message
        """

        loots = self.loot.list_loot()

        if loots:
            headers = ("Loot", "Path", "Time")
            self.tables.print_table("Collected Loot", headers, *loots)

        else:
            raise RuntimeWarning("No loot collected yet.")

    def show_module_databases(self) -> None:
        """ Show connected module databases.

        :return None: None
        :raises RuntimeWarning: with trailing warning message
        """

        databases = self.local_storage.get("connected_module_databases")

        if databases:
            databases_data = []
            number = 0
            headers = ("Number", "Name", "Path")

            for name in databases:
                databases_data.append(
                    (number, name, databases[name]['Path'])
                )
                number += 1

            self.tables.print_table("Connected Module Databases", headers, *databases_data)
        else:
            raise RuntimeWarning("No module databases connected.")

    def show_payload_databases(self) -> None:
        """ Show connected payload databases.

        :return None: None
        :raises RuntimeWarning: with trailing warning message
        """

        databases = self.local_storage.get("connected_payload_databases")

        if databases:
            databases_data = []
            number = 0
            headers = ("Number", "Name", "Path")

            for name in databases:
                databases_data.append(
                    (number, name, databases[name]['Path'])
                )
                number += 1

            self.tables.print_table("Connected Payload Databases", headers, *databases_data)
        else:
            raise RuntimeWarning("No payload databases connected.")

    def show_encoder_databases(self) -> None:
        """ Show connected encoder databases.

        :return None: None
        :raises RuntimeWarning: with trailing warning message
        """

        databases = self.local_storage.get("connected_encoder_databases")

        if databases:
            databases_data = []
            number = 0
            headers = ("Number", "Name", "Path")

            for name in databases:
                databases_data.append(
                    (number, name, databases[name]['Path'])
                )
                number += 1

            self.tables.print_table("Connected Encoder Databases", headers, *databases_data)
        else:
            raise RuntimeWarning("No encoder databases connected.")

    def show_plugin_databases(self) -> None:
        """ Show connected plugin databases.

        :return None: None
        :raises RuntimeWarning: with trailing warning message
        """

        databases = self.local_storage.get("connected_plugin_databases")

        if databases:
            databases_data = []
            number = 0
            headers = ("Number", "Name", "Path")

            for name in databases:
                databases_data.append(
                    (number, name, databases[name]['Path'])
                )
                number += 1

            self.tables.print_table("Connected Plugin Databases", headers, *databases_data)
        else:
            raise RuntimeWarning("No plugin databases connected.")

    def show_plugins(self) -> None:
        """ Show plugins.

        :return None: None
        :raises RuntimeWarning: with trailing warning message
        """

        all_plugins = self.plugins.get_plugins()
        headers = ("Number", "Plugin", "Name")

        plugin_shorts = {}
        number = 0

        for database in sorted(all_plugins):
            plugins_data = []
            plugins = all_plugins[database]

            for plugin in sorted(plugins):
                plugin = plugins[plugin]

                plugins_data.append(
                    (number, plugin['Plugin'], plugin['Name'])
                )

                plugin_shorts.update({
                    number: plugin['Plugin']
                })

                number += 1

            self.tables.print_table(f"Plugins ({database})", headers, *plugins_data)

        if plugin_shorts:
            self.local_storage.set("plugin_shorts", plugin_shorts)
        else:
            raise RuntimeWarning("No plugins available.")

    def show_encoders(self) -> None:
        """ Show encoders.

        :return None: None
        :raises RuntimeWarning: with trailing warning message
        """

        all_encoders = self.local_storage.get("encoders")
        headers = ("Number", "Encoder", "Name")

        encoder_shorts = {}
        number = 0

        for database in sorted(all_encoders):
            encoders_data = []
            encoders = all_encoders[database]

            for encoder in sorted(encoders):
                encoder = encoders[encoder]

                encoders_data.append(
                    (number, encoder['Encoder'], encoder['Name'])
                )

                encoder_shorts.update({
                    number: encoder['Encoder']
                })

                number += 1

            self.tables.print_table(f"Encoders ({database})", headers, *encoders_data)

        if encoder_shorts:
            self.local_storage.set("encoder_shorts", encoder_shorts)
        else:
            raise RuntimeWarning("No encoders available.")

    def show_modules(self, category: Optional[str] = None) -> None:
        """ Show modules by category.

        :param Optional[str] category: category
        :return None: None
        :raises RuntimeWarning: with trailing warning message
        """

        all_modules = self.local_storage.get("modules")
        headers = ("Number", "Category", "Module", "Rank", "Name")

        module_shorts = {}
        number = 0

        for database in sorted(all_modules):
            modules_data = []
            modules = all_modules[database]

            for module in sorted(modules):
                module = modules[module]

                if category:
                    if category == module['Category']:
                        modules_data.append(
                            (number, module['Category'], module['Module'],
                             module['Rank'], module['Name'])
                        )

                        module_shorts.update({
                            number: module['Module']
                        })

                        number += 1
                else:
                    modules_data.append(
                        (number, module['Category'], module['Module'],
                         module['Rank'], module['Name'])
                    )

                    module_shorts.update(
                        {number: module['Module']}
                    )

                    number += 1

            if category:
                self.tables.print_table(f"{category.title()} Modules ({database})", headers, *modules_data)
            else:
                self.tables.print_table(f"Modules ({database})", headers, *modules_data)

        if module_shorts:
            self.local_storage.set("module_shorts", module_shorts)
        else:
            raise RuntimeWarning("No modules available.")

    def show_payloads(self) -> None:
        """ Show payloads.

        :return None: None
        :raises RuntimeWarning: with trailing warning message
        """

        all_payloads = self.local_storage.get("payloads")
        headers = ("Number", "Payload", "Rank", "Name")

        payload_shorts = {}
        number = 0

        for database in sorted(all_payloads):
            payloads_data = []
            payloads = all_payloads[database]

            for payload in sorted(payloads):
                payload = payloads[payload]

                payloads_data.append(
                    (number, payload['Payload'], payload['Rank'],
                     payload['Name'])
                )

                payload_shorts.update({
                    number: payload['Payload']
                })

                number += 1

            self.tables.print_table(f"Payloads ({database})", headers, *payloads_data)

        if payload_shorts:
            self.local_storage.set("payload_shorts", payload_shorts)
        else:
            raise RuntimeWarning("No payloads available.")

    def show_search_plugins(self, keyword: str) -> None:
        """ Show plugins that contain the keyword.

        :param str keyword: keyword
        :return None: None
        """

        all_plugins = self.local_storage.get("plugins")
        headers = ("Number", "Plugin", "Name")

        plugin_shorts = {}
        number = 0

        for database in all_plugins:
            plugins_data = []
            plugins = all_plugins[database]

            for plugin in sorted(plugins):
                plugin = plugins[plugin]

                if keyword in plugin['Plugin'] or keyword in plugin['Name']:
                    name = plugin['Plugin'].replace(keyword, self.colors.RED + keyword + self.colors.END)

                    description = plugin['Name'].replace(
                        keyword, self.colors.RED + keyword + self.colors.END)

                    plugins_data.append(
                        (number, name, description)
                    )

                    plugin_shorts.update(
                        {number: plugin['Plugin']}
                    )

                    number += 1

            if plugins_data:
                self.tables.print_table(f"Plugins ({database})", headers, *plugins_data)

        if plugin_shorts:
            self.local_storage.set("plugin_shorts", plugin_shorts)

    def show_search_encoders(self, keyword: str) -> None:
        """ Show encoders that contain the keyword.

        :param str keyword: keyword
        :return None: None
        """

        all_encoders = self.local_storage.get("encoders")
        headers = ("Number", "Encoder", "Name")

        encoder_shorts = {}
        number = 0

        for database in all_encoders:
            encoders_data = []
            encoders = all_encoders[database]

            for encoder in sorted(encoders):
                encoder = encoders[encoder]

                if keyword in encoder['Encoder'] or keyword in encoder['Name']:
                    name = encoder['Encoder'].replace(
                        keyword, self.colors.RED + keyword + self.colors.END)

                    description = encoder['Name'].replace(
                        keyword, self.colors.RED + keyword + self.colors.END)

                    encoders_data.append(
                        (number, name, description)
                    )

                    encoder_shorts.update({
                        number: encoder['Encoder']
                    })

                    number += 1

            if encoders_data:
                self.tables.print_table(f"Encoders ({database})", headers, *encoders_data)

        if encoder_shorts:
            self.local_storage.set("encoder_shorts", encoder_shorts)

    def show_search_modules(self, keyword: str) -> None:
        """ Show modules that contain the keyword.

        :param str keyword: keyword
        :return None: None
        """

        all_modules = self.local_storage.get("modules")
        headers = ("Number", "Category", "Module", "Rank", "Name")

        module_shorts = {}
        number = 0

        for database in all_modules:
            modules_data = []
            modules = all_modules[database]

            for module in sorted(modules):
                module = modules[module]

                if keyword in module['Module'] or keyword in module['Name']:
                    name = module['Module'].replace(keyword, self.colors.RED + keyword + self.colors.END)

                    description = module['Name'].replace(
                        keyword, self.colors.RED + keyword + self.colors.END)

                    modules_data.append((number, module['Category'], name,
                                         module['Rank'], description))

                    module_shorts.update(
                        {number: module['Module']}
                    )

                    number += 1

            if modules_data:
                self.tables.print_table(f"Modules ({database})", headers, *modules_data)

        if module_shorts:
            self.local_storage.set("module_shorts", module_shorts)

    def show_search_payloads(self, keyword: str) -> None:
        """ Show payloads that contain the keyword.

        :param str keyword: keyword
        :return None: None
        """

        all_payloads = self.local_storage.get("payloads")
        headers = ("Number", "Payload", "Rank", "Name")

        payload_shorts = {}
        number = 0

        for database in all_payloads:
            payloads_data = []
            payloads = all_payloads[database]

            for payload in sorted(payloads):
                payload = payloads[payload]

                if keyword in payload['Payload'] or keyword in payload['Name']:
                    name = payload['Payload'].replace(
                        keyword, self.colors.RED + keyword + self.colors.END)

                    description = payload['Name'].replace(
                        keyword, self.colors.RED + keyword + self.colors.END)

                    payloads_data.append(
                        (number, name, payload['Rank'], description)
                    )

                    payload_shorts.update({
                        number: payload['Payload']
                    })

                    number += 1

            if payloads_data:
                self.tables.print_table(f"Payloads ({database})", headers, *payloads_data)

        if payload_shorts:
            self.local_storage.set("payload_shorts", payload_shorts)

    def show_sessions(self) -> None:
        """ Show opened sessions.

        :return None: None
        :raises RuntimeWarning: with trailing warning message
        """

        sessions = self.sessions.get_sessions()

        if sessions:
            sessions_data = []
            headers = ("ID", "Platform", "Arch", "Type", "Host", "Port")

            for session_id in sessions:
                session = sessions[session_id]

                platform = session['Platform']
                architecture = session['Arch']
                type = session['Type']
                host = session['Host']
                port = session['Port']

                sessions_data.append(
                    (session_id, platform, architecture, type, host, port)
                )

            self.tables.print_table("Opened Sessions", headers, *sessions_data)
        else:
            raise RuntimeWarning("No opened sessions available.")

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
        options_data = []

        for option in sorted(options):
            if options[option]['Visible']:
                value, required = options[option]['Value'], \
                    options[option]['Required']

                if required:
                    required = "yes"
                else:
                    required = "no"

                if isinstance(value, bool):
                    if value:
                        value = "yes"
                    else:
                        value = "no"

                options_data.append(
                    (option, "" if value is None else value, required, options[option]['Description'])
                )

        self.tables.print_table(title, headers, *options_data)

    def show_options(self) -> None:
        """ Show options.

        :return None: None
        :raises RuntimeWarning: with trailing warning message
        """

        module = self.modules.get_current_module()
        payload = self.payloads.get_current_payload(module)

        if not module:
            raise RuntimeWarning("No module selected.")

        if hasattr(module, "options"):
            self.show_options_table(f"Module Options ({module.details['Module']})", module.options)

        if payload:
            encoder = self.encoders.get_current_encoder(module, payload)

            if payload and hasattr(payload, "options"):
                self.show_options_table(f"Payload Options ({payload.details['Payload']})", payload.options)

            if encoder and hasattr(encoder, "options"):
                self.show_options_table(f"Encoder Options ({encoder.details['Encoder']})", encoder.options)

    def show_advanced(self) -> None:
        """ Show advanced options.

        :return None: None
        :raises RuntimeWarning: with trailing warning message
        """

        module = self.modules.get_current_module()
        payload = self.payloads.get_current_payload(module)

        if not module:
            raise RuntimeWarning("No module selected.")

        if hasattr(module, "advanced"):
            self.show_options_table(
                f"Module Advanced Options ({module.details['Module']})", module.advanced)

        if payload:
            encoder = self.encoders.get_current_encoder(module, payload)

            if payload and hasattr(payload, "advanced"):
                self.show_options_table(
                    f"Payload Advanced Options ({payload.details['Payload']})", payload.advanced)

            if encoder and hasattr(encoder, "advanced"):
                self.show_options_table(
                    f"Encoder Advanced Options ({encoder.details['Encoder']})", encoder.advanced)
